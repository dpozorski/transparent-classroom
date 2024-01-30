from transparent_classroom import models
from typing import Dict, List, Generic, TypeVar, Union, Type


_J = TypeVar('_J', bound=models.JSONModel)


class Deserializer(Generic[_J]):
    """
    Abstract Base Class for JSON Deserialization

    Attributes:


    """

    def __init__(self, cls: Type[_J]) -> None:
        """
        Deserializer Constructor

        :param cls: Type, The model type to deserialize.
        :return: None

        """

        self._cls = cls

    def deserialize(self, data: Dict) -> _J:
        """
        Method for deserializing the provided object data into the associated object.

        :param data: Dict, The object to serialize.
        :return: _J

        """

        return self._cls.from_dict(data=data)

    def batch(self, data: Union[Dict, List[Dict]]) -> List[_J]:
        """
        Batch deserialize the objects.

        :param data: Union[Dict, List[Dict]], The object to deserialize.
        :return: List[_J]

        """

        deserialized_objects = []
        data = data if isinstance(data, list) else [data]

        for obj_data in data:
            deserialized_objects.append(self.deserialize(data=obj_data))

        return deserialized_objects


class AuthDeserializer(Deserializer[models.Auth]):
    """
    Auth Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into auth objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Auth Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Auth)


class ActivityDeserializer(Deserializer[models.Activity]):
    """
    Activity Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into activity objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Activity Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Activity)


class ChildDeserializer(Deserializer[models.Child]):
    """
    Child Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into child objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Child Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Child)


class ClassroomDeserializer(Deserializer[models.Classroom]):
    """
    Classroom Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into classroom objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Classroom Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Classroom)


class ConferenceReportDeserializer(Deserializer[models.ConferenceReport]):
    """
    Conference Report Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into conference report objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Conference Report Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.ConferenceReport)

    def deserialize(self, data: Dict) -> models.ConferenceReport:
        """
        Method for deserializing the provided object data into a conference report object.

        :param data: Dict, The object to serialize.
        :return: models.Form

        TODO:
            - Parse data component

        """

        formatted_data = {
            "id": data.get("id", None),
            "name": data.get("name", None),
            "child_id": data.get("child_id", None),
            "data": data.get("data", None)
        }

        return super().deserialize(data=formatted_data)


class EventDeserializer(Deserializer[models.Event]):
    """
    Event Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into event objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Event Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Event)


class FormDeserializer(Deserializer[models.Form]):
    """
    Form Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into form (response) objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Form (Response) Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Form)

    def deserialize(self, data: Dict) -> models.Form:
        """
        Method for deserializing the provided object data into a form (response) object.

        :param data: Dict, The object to serialize.
        :return: models.Form

        """

        formatted_data = {
            "id": data.get("id", None),
            "form_template_id": data.get("form_template_id", None),
            "state": data.get("state", None),
            "child_id": data.get("child_id", None),
            "created_at": data.get("created_at", None)
        }

        if "fields" in data.keys():
            fields = data["fields"]
            formatted_data["student_first_name"] = fields.get("Student Name.first", None)
            formatted_data["student_last_name"] = fields.get("Student Name.last", None)
            formatted_data["classroom"] = fields.get("Classroom", None)
            formatted_data["parent_name"] = fields.get("Parent Name", None)
            formatted_data["signature"] = fields.get("Signature", None)
            formatted_data["release"] = fields.get("Photo and Documentation Release ", None)

        return super().deserialize(data=formatted_data)


class FormTemplateDeserializer(Deserializer[models.FormTemplate]):
    """
    Form Template Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into form template objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Form Template Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.FormTemplate)

    def deserialize(self, data: Dict) -> models.FormTemplate:
        """
        Method for deserializing the provided object data into a form template object.

        :param data: Dict, The object to serialize.
        :return: models.FormTemplate

        TODO:
            - Will have to deserialize widget object(s).

        """

        return super().deserialize(data=data)


class LessonSetDeserializer(Deserializer[models.LessonSet]):
    """
    Lesson Set Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into lesson set objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Lesson Set Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.LessonSet)

    def deserialize(self, data: Dict) -> models.LessonSet:
        """
        Method for deserializing the provided object data into a lesson set object.

        :param data: Dict, The object to serialize.
        :return: models.Form

        TODO:
            - Parse children component in lesson sets/lessons

        """

        formatted_data = {
            "id": data.get("id", None),
            "name": data.get("name", None),
            "children": data.get("children", None)
        }

        return super().deserialize(data=formatted_data)


class LevelDeserializer(Deserializer[models.Level]):
    """
    Level Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into level objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Level Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Level)


class OnlineApplicationDeserializer(Deserializer[models.OnlineApplication]):
    """
    Online Application Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into online application objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Online Application Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.OnlineApplication)

    def deserialize(self, data: Dict) -> models.OnlineApplication:
        """
        Method for deserializing the provided object data into an online application object.

        :param data: Dict, The object to serialize.
        :return: models.OnlineApplication

        """

        formatted_data = {
            "id": data["id"],
            "school_id": data["school_id"],
            "state": data["state"]
        }

        if "fields" in data.keys():
            fields = data["fields"]
            formatted_data["program"] = fields.get("program", None)
            formatted_data["child_first_name"] = fields.get("child_name.first", None)
            formatted_data["child_last_name"] = fields.get("child_name.last", None)
            formatted_data["child_birth_date"] = fields.get("child_birth_date", None)
            formatted_data["child_gender"] = fields.get("child_gender", None)
            formatted_data["mother_email"] = fields.get("mother_email", None)
            formatted_data["session_id"] = fields.get("session_id", None)

        return super().deserialize(data=formatted_data)


class SchoolDeserializer(Deserializer[models.School]):
    """
    School Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into school objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        School Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.School)


class SessionDeserializer(Deserializer[models.Session]):
    """
    Session Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into session objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Session Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Session)


class UserDeserializer(Deserializer[models.User]):
    """
    User Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into user objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        User Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.User)
