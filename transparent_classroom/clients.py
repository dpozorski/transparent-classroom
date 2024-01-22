import requests
from datetime import date, datetime
from transparent_classroom import apis
from typing import Optional, List, Dict
from transparent_classroom.api.enums import HTTPMethod
from transparent_classroom.api.entry_points import EntryPoint
from transparent_classroom.api.enums import ModelType, EndpointBehavior


class Client(object):
    """
    Client Class

    Attributes:
        email (`str`): The email of the account to use for authenticating
            to Transparent Classroom.
        password (`str`): The password of the account to use for
            authenticating to Transparent Classroom.
        host (`str`): The root url of the host of the API.
        masquerade_id (`int`): As an admin, you can act as another user
            by setting this header to the user's ID.
        school_id (`int`): As a network admin, you can act on behalf of a
            school in your network by setting this header to the school's ID.

    """

    """
    The default Transparent Classroom host address
    
    """
    __DEFAULT_HOST = "https://www.transparentclassroom.com"

    def __init__(
            self,
            email: str,
            password: str,
            host: Optional[str] = None,
            masquerade_id: Optional[int] = None,
            school_id: Optional[int] = None) -> None:
        """
        Transparent Classroom Client Constructor

        :param email: str, The email of the account to use for authenticating
            to Transparent Classroom.
        :param password: str, The password of the account to use for
            authenticating to Transparent Classroom.
        :param masquerade_id: Optional[int], As an admin, you can act as another
            user by setting this header to the user's ID.
        :param school_id: Optional[int], As a network admin, you can act on behalf
            of a school in your network by setting this header to the school's ID.
        :param host: Optional[str], The root url of the host of the API.
        :return: None

        """

        self.__token = None
        self.email = email
        self.password = password
        self.__api = apis.api
        self.masquerade_id = masquerade_id
        self.school_id = school_id
        self.host = host

    @staticmethod
    def __request(context: Dict) -> requests.Response:
        """
        Send the request to the API.

        :param context: Dict, The dictionary containing the headers, parameters, and
            other request metadata to include with the request.
        :return: requests.Response

        """

        kwargs = {
            "headers": context["headers"],
            "params": context["parameters"],
            "auth": context["auth"] if "auth" in context.keys() else None
        }

        if context["method"] == HTTPMethod.POST:
            return requests.post(context["url"], **kwargs)
        elif context["method"] == HTTPMethod.PUT:
            return requests.put(context["url"], **kwargs)
        else:
            return requests.get(context["url"], **kwargs)

    def __get_context(self, entry_point: EntryPoint, parameters: Dict, route_parameters: Dict) -> Dict:
        """
        Validate and return the validated context data for the entry point.

        :param entry_point: EntryPoint, The entry point of the API.
        :param parameters: Dict, The parameters to send to the entry point (Transparent Classroom).
        :param route_parameters: Dict, The route parameters used to build/customize the route.
        :return: Dict

        """

        if ("model_name" not in route_parameters.keys()) or (route_parameters["model_name"] is None):
            route_parameters["model_name"] = entry_point.model_type.value

        context = entry_point.interface.validate(headers=self.headers, parameters=parameters)
        context["url"] = "/".join([self.host, entry_point.route.apply(**route_parameters)])
        context["method"] = entry_point.interface.method
        return context

    def __submit(
            self,
            model_type: ModelType,
            behavior: EndpointBehavior,
            parameters: Dict,
            route_parameters: Optional[Dict] = None) -> requests.Response:
        """
        Route the kwargs to the relevant entrypoint, build the request, and submit
        the request to the API.

        :param model_type: ModelType, The API model type to interacted with.
        :param behavior: EndpointBehavior, The expected behavior of the endpoint.
        :param parameters: Dict, The params to provide to the entry point.
        :param route_parameters: Optional[Dict], The params to provide for updating the route.
        :return: requests.Response

        """

        if (self.token is None) and (model_type is not ModelType.AUTHENTICATE):
            self.authenticate()

        entry_point = self.__api.route(model_type=model_type, behavior=behavior)
        context = self.__get_context(entry_point=entry_point, parameters=parameters, route_parameters=route_parameters)
        return self.__request(context=context)

    def authenticate(self) -> None:
        """
        Authenticate the client with Transparent Classroom.

        :return: None

        TODO:
            - Also get role data

        """

        response = self.__submit(**{
            "model_type": ModelType.AUTHENTICATE,
            "behavior": EndpointBehavior.SHOW,
            "parameters": {
                "email": self.email,
                "password": self.password
            },
            "route_parameters": {

            }
        })

    def get_activities(
            self,
            child_id: Optional[int] = None,
            classroom_id: Optional[int] = None,
            only_photos: Optional[bool] = False,
            only_portfolio: Optional[bool] = False,
            date_start: Optional[date] = None,
            date_end: Optional[date] = None,
            page: Optional[int] = 1,
            per_page: Optional[int] = 50) -> List:
        """
        Get all the activities (possibly filtered by child or classroom).

        :param child_id: Optional[int], The id of the child to show observations,
            presentations, and/or photos for.
        :param classroom_id: Optional[int], The id of the classroom to show observations,
            presentations, and/or photos for.
        :param only_photos: Optional[bool], Flag indicating that only photos should
            be returned.
        :param only_portfolio: Optional[bool], Flag indicating that only portfolio items
            should be returned.
        :param date_start: Optional[date], Filter parameter to only return records on/after
            this date. (format: 2016-05-01)
        :param date_end: Optional[date], Filter parameter to only return records on/before
            this date. (format: 2016-05-01)
        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        :raises: ValueError

        """

        if (child_id is None) and (classroom_id is None):
            raise ValueError("Either a child_id or classroom_id value needs to be provided.")

        response = self.__submit(**{
            "model_type": ModelType.ACTIVITY,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "child_id": child_id,
                "classroom_id": classroom_id,
                "only_photos": only_photos,
                "only_portfolio": only_portfolio,
                "date_start": date_start,
                "date_end": date_end,
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_child(self, child_id: int, as_of: Optional[date] = None) -> Dict:
        """
        Get the specified child data.

        :param child_id: int, The id of the child to get the data for.
        :param as_of: Optional[date], If specified, shows child fields as of this date
        :return: Dict

        """

        response = self.__submit(**{
            "model_type": ModelType.CHILDREN,
            "behavior": EndpointBehavior.SHOW,
            "parameters": {
                "as_of": as_of
            },
            "route_parameters": {
                "object_id": child_id
            }
        })

    def get_children(
            self,
            classroom_id: Optional[int] = None,
            session_id: Optional[int] = None,
            only_current: Optional[bool] = False,
            page: Optional[int] = 1,
            per_page: Optional[int] = 50) -> List:
        """
        Get all the children (possibly filtered by classroom, session, and/or recency).

        :param classroom_id: Optional[int], The id of the classroom to use when filtering
            children to show. Required for teachers, optional for admin staff.
        :param session_id: Optional[int], The id of the session to filter the children by.
            Will use the current session as the filter, if None provided.
        :param only_current: Optional[bool], Flag indicating that only currently enrolled
            children will be returned.
        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.CHILDREN,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "classroom_id": classroom_id,
                "session_id": session_id,
                "only_current": only_current,
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_classrooms(
            self,
            show_inactive: Optional[bool] = False,
            page: Optional[int] = 1,
            per_page: Optional[int] = 50) -> List:
        """
        Get all the available/registered classrooms at the school.

        :param show_inactive: Optional[bool], Flag indicating whether inactive classrooms
            should be returned in the response.
        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.CLASSROOMS,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "show_inactive": show_inactive,
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_conference_reports(
            self,
            child_id: Optional[int] = None,
            created_after: Optional[date] = None,
            created_before: Optional[date] = None,
            page: Optional[int] = 1,
            per_page: Optional[int] = 50) -> List:
        """
        Get all the available/registered classrooms at the school.

        :param child_id: Optional[int], The id of the child to filter conference reports for.
        :param created_after: Optional[date], Only show reports created after date (format: 2016-05-01)
        :param created_before: Optional[date], Only show reports created before date (format: 2016-04-01)
        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.CONFERENCE_REPORTS,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "child_id": child_id,
                "created_after": created_after,
                "created_before": created_before,
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_form(self, form_id: int) -> Dict:
        """
        Get the specified form instance's response data (i.e. an individual response
        to a form template).

        :param form_id: int, The id of the form response to get.
        :return: Dict

        """

        response = self.__submit(**{
            "model_type": ModelType.FORMS,
            "behavior": EndpointBehavior.SHOW,
            "parameters": {

            },
            "route_parameters": {
                "object_id": form_id
            }
        })

    def get_forms(
            self,
            form_template_id: Optional[int] = None,
            child_id: Optional[int] = None,
            created_before: Optional[date] = None,
            created_after: Optional[date] = None,
            page: Optional[int] = 1,
            per_page: Optional[int] = 50) -> List:
        """
        Get all the form responses with the optional filtering.

        :param form_template_id: Optional[int], The id of the form template/type to filter by.
        :param child_id: Optional[int], The id of the child to filter form responses by.
        :param created_after: Optional[date], Filter to only form responses created before a certain date.
        :param created_before: Optional[date], Filter to only form responses created after a certain date.
        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.FORMS,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "form_template_id": form_template_id,
                "child_id": child_id,
                "created_after": created_after,
                "created_before": created_before,
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_form_templates(self, page: Optional[int] = 1, per_page: Optional[int] = 50) -> List:
        """
        Get all the form templates (their metadata, widgets, etc.).

        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.FORM_TEMPLATES,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_lesson_set(self, lesson_set_id: int, format: Optional[str] = "short") -> Dict:
        """
        Get the lesson set and all the associated lessons in the lesson set.

        :param lesson_set_id: int, The id of the lesson set to get.
        :param format: Optional[str], Format of the lesson set description. Long will include
            photos and descriptions, defaults to short [long, short].
        :return: Dict

        """

        response = self.__submit(**{
            "model_type": ModelType.LESSON_SETS,
            "behavior": EndpointBehavior.SHOW,
            "parameters": {
                "format": format
            },
            "route_parameters": {
                "object_id": lesson_set_id
            }
        })

    def get_online_application(self, online_application_id: int) -> Dict:
        """
        Get the form data of the specified online application.

        :param online_application_id: int, The id of the online application to get.
        :return: Dict

        """

        response = self.__submit(**{
            "model_type": ModelType.ONLINE_APPLICATIONS,
            "behavior": EndpointBehavior.SHOW,
            "parameters": {

            },
            "route_parameters": {
                "object_id": online_application_id
            }
        })

    def get_online_applications(
            self,
            created_at: Optional[datetime] = None,
            page: Optional[int] = 1,
            per_page: Optional[int] = 50) -> List:
        """
        Get all the online application responses (optionally filtered to include all responses
        after the provided created_at datetime value).

        :param created_at: Optional[date], Filter to only include online applications completed
            on or after the specified datetime.
        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.ONLINE_APPLICATIONS,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "created_at": created_at,
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_schools(self, page: Optional[int] = 1, per_page: Optional[int] = 50) -> List:
        """
        Get all the schools registered within the network on Transparent Classroom.

        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.SCHOOLS,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_sessions(self, page: Optional[int] = 1, per_page: Optional[int] = 50) -> List:
        """
        Get all the schools registered within the network on Transparent Classroom.

        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.SESSIONS,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    def get_user(self, user_id: int) -> Dict:
        """
        Get the specified user's details.

        :param user_id: int, The id of the user to get.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.USERS,
            "behavior": EndpointBehavior.SHOW,
            "parameters": {

            },
            "route_parameters": {
                "object_id": user_id
            }
        })

    def get_users(
            self,
            classroom_id: Optional[int] = None,
            roles: Optional[List] = None,
            page: Optional[int] = 1,
            per_page: Optional[int] = 50) -> List:
        """
        Get all the users in Transparent Classroom (potentially filtered using the available
        method parameters).

        :param classroom_id: Optional[int], Filter the response to only include users that have
            an affiliation with the specified classroom id (required for teachers).
        :param roles: Optional[List], Filter the response to include users matching any of the
            roles included in the request (teacher, parent, admin, billing_manager, family_member).
        :param page: Optional[int], The result page to paginate to.
        :param per_page: Optional[int], The number of records to return on the paginated page.
        :return: List

        """

        response = self.__submit(**{
            "model_type": ModelType.USERS,
            "behavior": EndpointBehavior.LIST,
            "parameters": {
                "classroom_id": classroom_id,
                "roles": roles,
                "page": page,
                "per_page": per_page
            },
            "route_parameters": {

            }
        })

    @property
    def email(self) -> str:
        """
        Email accessor method.

        :return: str

        """

        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """
        Email setter method.

        :param value: str, The value to set the email attribute to.
        :return: None

        """

        self.__token = None
        self._email = value

    @property
    def password(self) -> str:
        """
        Password accessor method.

        :return: str

        """

        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """
        Password setter method.

        :param value: str, The value to set the password attribute to.
        :return: None

        """

        self.__token = None
        self._password = value

    @property
    def masquerade_id(self) -> int:
        """
        Get the masquerade id.

        :return: int

        """

        return self._masquerade_id

    @masquerade_id.setter
    def masquerade_id(self, value: int) -> None:
        """
        Set the masquerade id (the user id to masquerade as), if the
        provided credentials are associated with an admin account.

        :param value: int, The masquerade id.
        :return: None

        """

        self._masquerade_id = value

    @property
    def school_id(self) -> int:
        """
        Get the school id.

        :return: int

        """

        return self._school_id

    @school_id.setter
    def school_id(self, value: int) -> None:
        """
        As a network admin, you can act on behalf of a school in your
        network by setting this header to the school's ID.

        :param value: int, The school id.
        :return: None

        """

        self._school_id = value

    @property
    def token(self) -> str:
        """
        The access token retrieved from Transparent Classroom.

        :return: str

        """

        return self.__token

    @property
    def host(self) -> str:
        """
        Get the root host server address of the API.

        :return: str

        """

        return self.__DEFAULT_HOST if self._host is None else self._host

    @host.setter
    def host(self, value: str) -> None:
        """
        Set the API host address.

        :param value: str, The API root host address.
        :return: None

        """

        self._host = self.__DEFAULT_HOST if value is None else value.rstrip("/")

    @property
    def headers(self) -> Dict:
        """
        Get the header values used by the client when making requests.

        :return: Dict

        """

        return {
            "X-TransparentClassroomToken": "test",  # self.token,
            "X-TransparentClassroomMasqueradeId": self.masquerade_id,
            "X-TransparentClassroomSchoolId": self.school_id
        }


client = Client(email="t", password="b")
client.get_schools()
