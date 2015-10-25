"""Procedures to initialize the full text search in PostgresQL"""

import psycopg2
from django.db import connection, connections
from django.utils.encoding import force_text
from django.utils.translation import get_language


# mapping of "django" language names to postgres
LANGUAGE_NAMES = {
    'da': 'danish',
    'de': 'german',
    'en': 'english',
    'es': 'spanish',
    'fi': 'finnish',
    'fr': 'french',
    'hu': 'hungarian',
    'it': 'italian',
    'ja': 'japanese',
    'nb': 'norwegian',
    'nl': 'dutch',
    'pt': 'portugese',
    'ro': 'romanian',
    'ru': 'russian',
    'sv': 'swedish',
    'tr': 'turkish',
    'kr': 'korean',
    'zh-cn': 'chinese',
}


def setup_full_text_search(script_path):
    """using postgresql database connection,
    installs the plsql language, if necessary
    and runs the stript, whose path is given as an argument
    """
    fts_init_query = open(script_path).read()

    cursor = connection.cursor()
    try:
        # test if language exists
        cursor.execute("SELECT * FROM pg_language WHERE lanname='plpgsql'")
        lang_exists = cursor.fetchone()
        if not lang_exists:
            cursor.execute("CREATE LANGUAGE plpgsql")
        # run the main query
        cursor.execute(fts_init_query)
    finally:
        cursor.close()


def run_full_text_search(query_set, query_text, text_search_vector_name):
    """runs full text search against the query set and
    the search text. All words in the query text are
    added to the search with the & operator - i.e.
    the more terms in search, the narrower it is.

    It is also assumed that we ar searching in the same
    table as the query set was built against, also
    it is assumed that the table has text search vector
    stored in the column called with value of`text_search_vector_name`.
    """
    table_name = query_set.model._meta.db_table

    rank_clause = 'ts_rank(' + table_name + '.' + text_search_vector_name + ', plainto_tsquery(%s, %s))'

    where_clause = table_name + '.' + text_search_vector_name + ' @@ plainto_tsquery(%s, %s)'

    language_code = get_language()

    # a hack with japanese search for the short queries
    if language_code in ['ja', 'zh-cn'] and len(query_text) in (1, 2):
        mul = int(4 / len(query_text))  # 4 for 1 and 2 for 2
        query_text = (query_text + ' ')*mul

    search_query = '|'.join(query_text.split())  # apply "OR" operator
    language_name = LANGUAGE_NAMES.get(language_code, 'english')
    extra_params = (language_name, search_query,)
    extra_kwargs = {
        'select': {'relevance': rank_clause},
        'where': [where_clause],
        'params': extra_params,
        'select_params': extra_params,
    }

    return query_set.extra(**extra_kwargs)


def run_thread_search(query_set, query):
    """runs search for full thread content"""
    return run_full_text_search(query_set, query, 'text_search_vector')


run_user_search = run_thread_search  # an alias


def run_title_search(query_set, query):
    """runs search for title and tags"""
    return run_full_text_search(query_set, query, 'title_search_vector')


class QuerySetSearchMixIn(object):
    #
    # https://github.com/linuxlewis/djorm-ext-pgfulltext/blob/master/djorm_pgfulltext/models.py#L242
    #
    @property
    def manager(self):
        return self.model._fts_manager

    @property
    def db(self):
        return self._db or self.manager.db

    def search(self, query, rank_field=None, rank_function='ts_rank', config=None, rank_normalization=32, raw=False,
               using=None, fields=None, headline_field=None, headline_document=None):
        if not config:
            config = self.manager.config

        db_alias = using if using is not None else self.db
        connection = connections[db_alias]
        qn = connection.ops.quote_name

        qs = self
        if using is not None:
            qs = qs.using(using)

        if query:
            function = 'to_tsquery' if raw else 'plainto_tsquery'
            ts_query = "{}('{}', '{}')".format(function, config, force_text(query))  # TODO: psycopg2.extensions.adapt
            # ts_query = "{}('{}', '{}')".format(function, config, psycopg2.extensions.adapt(force_text(query)))
            full_search_field = "{}.{}".format(qn(self.model._meta.db_table), qn(self.manager.search_field))

            # if fields is passed, obtain a vector expression with these fields. In other case, intent use of
            # search_field if exists.
            if fields:
                search_vector = self.manager._get_search_vector(config, using, fields=fields)
            else:
                if not self.manager.search_field:
                    raise ValueError('search_field is not specified.')
                search_vector = full_search_field

            where = ' ({}) @@ ({})'.format(search_vector, ts_query)
            select_dict, order_by = {}, []

            if rank_field:
                select_dict[rank_field] = '{}({}, {}, {})'.format(rank_function, search_vector, ts_query,
                                                                  rank_normalization)
                order_by = ['-{}'.format(rank_field)]

            if headline_field is not None and headline_document is not None:
                select_dict[headline_field] = "ts_headline('{}', '{}', '{}')".format(config, headline_document,
                                                                                     ts_query)

            qs = qs.extra(select=select_dict, where=[where], order_by=order_by)

        return qs

