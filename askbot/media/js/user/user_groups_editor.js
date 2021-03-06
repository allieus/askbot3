/**
 * @constructor
 * allows editing user groups
 */
var UserGroupsEditor = function () {
    WrappedElement.call(this);
};
inherits(UserGroupsEditor, WrappedElement);

UserGroupsEditor.prototype.decorate = function (element) {
    this._element = element;
    var add_link = element.find('#add-group');
    var adder = new GroupAdderWidget();
    adder.decorate(add_link);

    var groups_container = new GroupsContainer();
    groups_container.decorate(element.find('#groups-list'));
    adder.setGroupsContainer(groups_container);
    //TODO - add group deleters
};
