from abc import ABC
from typing import Dict, Any


class UnitOfWorkMixin(ABC):
    """
    A mixin which makes a class provide Unit of Work functionality if you derive from it
    """
    def __init__(self):
        self.__dirty_attributes: Dict = {}

    def is_dirty(self, attribute_name) -> bool:
        """
        Checks if an attribute has been changed
        :param attribute_name: the name of the attribute to be checked
        :return: True if this attribute has been changed, False if not
        """
        if attribute_name in self.__dirty_attributes:
            if self.__dirty_attributes[attribute_name]["new"] is True:
                return False
            else:
                return True
        else:
            return False

    def old_value(self, attribute_name: str) -> Any:
        """
        query the old value before the change
        :param attribute_name: The name of the changed attribute
        :return: the old value before the change
        :raise ValueError: if this attribute has not been changed
        """
        if not self.is_dirty(attribute_name):
            raise ValueError("Attribute is not Dirty")
        return self.__dirty_attributes[attribute_name]["old_value"]

    def get_attribute_name(self, attribute_value: Any):
        """
        Query the name of the attribute by passing this attribute's value
        :param attribute_value: The attribute's value the name is queried for
        :return: the attribute's name
        """
        attr_type = type(attribute_value)
        attr_id = id(attribute_value)
        for itemname, itemvalue in self.__dict__.items():
            if id(itemvalue) == attr_id:
                return itemname

    def get_dirty_attributes_names(self) -> [str]:
        """
        Get a the names of the attributes which have been changed
        :return: The names of the attributes
        """
        if self.__dirty_attributes == {}:
            return []
        dirty_attributes: list = []
        for attribute_name in self.__dirty_attributes.keys():
            dirty_attributes.append(attribute_name)
        return dirty_attributes

    def get_dirty_attributes(self) -> Dict[str, Dict[str, Any]]:
        """
        get all changed attributes incuding their respective old and new values
        :return: all changed attributes
        """
        if self.__dirty_attributes == {}:
            return self.__dirty_attributes
        dirty_attributes: Dict[str, Dict[str, Any]] = {}
        for attribute in self.__dirty_attributes:
            dirty_attributes[attribute] = {"old_value": self.__dirty_attributes[attribute]["old_value"],
                                           "new_value": self.__dirty_attributes[attribute]["new_value"]}
        return dirty_attributes

    def commit(self):
        self.__dict__["_UnitOfWorkMixin__dirty_attributes"] = {}

    def rollback(self):
        for attribute in self.__dirty_attributes:
            self.__dict__[attribute] = self.__dirty_attributes[attribute]["old_value"]
        self.__dict__["_UnitOfWorkMixin__dirty_attributes"] = {}

    def __setattr__(self, attribute: str, value):
        if hasattr(self, attribute):
            if self.__getattribute__(attribute) is None:
                self.__dirty(attribute, False, value, None)
                self.__dict__[attribute] = value
            else:
                self.__update_attribute(attribute, value)
        else:
            self.__create_attribute(attribute, value)

    def __update_attribute(self, attribute_name: str, value):
        """
        Update an attribute
        :param attribute_name: the attribute's name
        :param value: the attrbie's new value
        :return:
        """
        old_value = getattr(self, attribute_name)
        self.__dirty(attribute_name, False, value, old_value)
        self.__dict__[attribute_name] = value

    def __create_attribute(self, attribute: str, value):
        """
        create a new Attribute for this class
        :param attribute: the attribute's name
        :param value: the attribute's value
        """
        self.__dict__[attribute] = value

    def __dirty(self, attribute_name: str, new: bool, new_value, old_value=None):
        """
        Mark an attribute as dirty
        :param attribute_name: the attributes name
        :param new: if an attribute is newly created
        :param new_value: the attribute's updated value
        :param old_value: the attributes old value
        """
        self.__dirty_attributes[attribute_name] = {"old_value": old_value, "new_value": new_value, "new": new}
