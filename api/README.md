
# Endpoints

**Note**: The base URL for all the following endpoints is: `/api`

## Table of contents
- [User Related Endpoints](#user-related-endpoints)
	- [User create](#user-create)
	- [Current user retrieve](#current-user-retrieve)
	- [Current user update](#current-user-update)
	- [Login / Token create](#login--token-create)
	- [Logout / Token destroy](#logout--token-destroy)
- [Authority Related Endpoints](#authority-related-endpoints)
  - [Authority enroll](#authority-enroll)
- [School Related Endpoints](#school-related-endpoints)
  - [School enroll](#school-enroll)

# User Related Endpoints

## User create

Use this endpoint to register a new user. 

**URL**: `/users/`

**Method**: `POST`

### Request Parameters
|Parameter|Description  |
|--|--|
|`username`|Username of the user to be created. Returns a `HTTP_400_BAD_REQUEST` if there is another user with same username.  |
|`email`|Email of the user to be created. Returns a `HTTP_400_BAD_REQUEST` if there is another user with same email.|
|`password`|Password of the user to be created.|

### Response Parameters
|Parameter|Description|
|--|--|
|`status`|`HTTP_201_CREATED`|
|`id`|ID of the user just created|
|`username`|Username of the user|
|`email`|Email of the user|

## Current user retrieve

Use this endpoint to retrieve the details of the currently logged in user.

**URL**: `/users/me/`

**Method**: `GET`
**_Requires_**: Auth token to be passed in the header

### Response Parameters
|Parameter|Description|
|--|--|
|`status`|`HTTP_200_OK`|
|`id`|ID of the user logged in|
|`username`|Username of the user|
|`email`|Email of the user|


## Current user update

Use this endpoint to update the details of the currently logged in user.

**URL**: `/users/me/`

**Method**: `PUT` or `PATCH`

**_Requires_**: Auth token to be passed in the header

### Request Parameters
|Parameter|Description  |
|--|--|
|`username`|Username of the user to be updated. Returns a `HTTP_400_BAD_REQUEST` if there is another user with same username.  |
|`email`|Email of the user to be updated. Returns a `HTTP_400_BAD_REQUEST` if there is another user with same email.|
|`password`|Password of the user to be created.|

### Response Parameters
|Parameter|Description|
|--|--|
|`status`|`HTTP_201_CREATED`|
|`id`|ID of the user logged in|
|`username`|Username of the user|
|`email`|Email of the user|

## Login / Token create

Use this endpoint to obtain user [authentication token](http://www.django-rest-framework.org/api-guide/authentication#tokenauthentication).

**URL**: `/token/login/`

**Method**: `POST`

### Request Parameters
|Parameter|Description  |
|--|--|
|`username`|Username|
|`password`|Password|

### Response Parameters
|Parameter|Description|
|--|--|
|`status`|`HTTP_200_OK`|
|`auth_token`|Auth token for the logged in user|

## Logout / Token destroy

Use this endpoint to logout user (remove user authentication token).
**URL**: `/token/logout/`

**Method**: `POST`

### Request Parameters

None

### Response Parameters
|Parameter|Description|
|--|--|
|`status`|`HTTP_204_NO_CONTENT`|


# Authority Related Endpoints

## Enroll authority

Use this endpoint to enroll the current user as an authority

**URL**: `/authority/`

**Method**: `POST`

**_Requires_**: Auth token of the user to be passed in the header. 

### Request Parameters
|Parameter|Description  |
|--|--|
|`district`|ID of the district the authority belongs to|


### Response Parameters
|Parameter|Description|
|--|--|
|`status`|`HTTP_201_CREATED`|
|`district`|ID of the district the authority belongs to|

# School Related Endpoints

## Enroll school

Use this endpoint to enroll the current user as an authority

**URL**: `/school/`

**Method**: `POST`

**_Requires_**: Auth token of the user to be passed in the header. 

### Request Parameters
|Parameter|Description  |
|--|--|
|`name`|Name of the school|
|`district`|ID of the district the school belongs to|


### Response Parameters
|Parameter|Description|
|--|--|
|`status`|`HTTP_201_CREATED`|
|`name`|Name of the school|
|`district`|ID of the district the school belongs to|


