wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/4.3.0/openapi-generator-cli-4.3.0.jar -O openapi-generator-cli.jar
sudo apt install openjdk-11-jdk


java -jar openapi-generator-cli.jar generate -i https://raw.githubusercontent.com/openapitools/openapi-generator/master/modules/openapi-generator/src/test/resources/2_0/petstore.yaml -g python-flask -o ./output/python-flask


https://editor.swagger.io/

```
openapi: 3.0.1
info:
  description: This is a sample server Petstore server. For this sample, you can use
    the api key `special-key` to test the authorization filters.
  license:
    name: Apache-2.0
    url: https://www.apache.org/licenses/LICENSE-2.0.html
  title: OpenAPI BsvContent
  version: 1.0.0
servers:
- url: https://bsvcontent.herokuapp.com/v1
tags:
- description: Everything about your Pets
  name: pet
- description: Access to Petstore orders
  name: store
- description: Operations about user
  name: user
paths:
  /api/upload_text:
    post:
      operationId: api_upload_text
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RequestUploadTextModel'
        description: Pet object that needs to be added to the store
        required: true
      responses:
        "405":
          content: {}
          description: Invalid input
      security:
      - petstore_auth:
        - write:pets
        - read:pets
      summary: Add a new pet to the store
      tags:
      - pet
      x-codegen-request-body-name: body
      x-openapi-router-controller: openapi_server.controllers.pet_controller
  /api/tx:
    get:
      description: Multiple status values can be provided with comma separated strings
      operationId: find_pets_by_status
      parameters:
      - description: Status values that need to be considered for filter
        explode: false
        in: path
        name: addr
        required: true
        schema:
          type: string
      responses:
        "200":
          content:
            application/xml:
              schema:
                items:
                  $ref: '#/components/schemas/RequestAddressModel'
                type: array
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/RequestAddressModel'
                type: array
          description: successful operation
        "400":
          content: {}
          description: Invalid status value
      security:
      - petstore_auth:
        - write:pets
        - read:pets
      summary: Finds Pets by status
      tags:
      - pet
      x-openapi-router-controller: openapi_server.controllers.pet_controller
  /api/add_address:
    post:
      operationId: place_order
      requestBody:
        content:
          '*/*':
            schema:
              $ref: '#/components/schemas/RequestAddressModel'
        description: order placed for purchasing the pet
        required: true
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RequestAddressModel'
          description: successful operation
        "400":
          content: {}
          description: Invalid Order
      summary: Place an order for a pet
      tags:
      - store
      x-codegen-request-body-name: body
      x-openapi-router-controller: openapi_server.controllers.store_controller

components:
  schemas:
    RequestUploadTextModel:
      description: An order for a pets from the pet store
      example:
        petId: 6
        quantity: 1
        id: 0
        shipDate: 2000-01-23T04:56:07.000+00:00
        complete: false
        status: placed
      properties:
        id:
          format: int64
          type: integer
        petId:
          format: int64
          type: integer
        quantity:
          format: int32
          type: integer
        shipDate:
          format: date-time
          type: string
        status:
          description: Order Status
          enum:
          - placed
          - approved
          - delivered
          type: string
        complete:
          default: false
          type: boolean
      title: Pet Order
      type: object
      xml:
        name: Order
    RequestAddressModel:
      description: A category for a pet
      example:
        name: address
      properties:
        name:
          type: string
      title: Pet category
      type: object
    ApiResponse:
      description: Describes the result of uploading an image resource
      example:
        code: 0
        type: type
        message: message
      properties:
        code:
          format: int32
          type: integer
        type:
          type: string
        message:
          type: string
      title: An uploaded response
      type: object
  securitySchemes:
    petstore_auth:
      flows:
        implicit:
          authorizationUrl: http://petstore.swagger.io/api/oauth/dialog
          scopes:
            write:pets: modify pets in your account
            read:pets: read your pets
      type: oauth2
      x-tokenInfoFunc: openapi_server.controllers.security_controller_.info_from_petstore_auth
      x-scopeValidateFunc: openapi_server.controllers.security_controller_.validate_scope_petstore_auth
    api_key:
      in: header
      name: api_key
      type: apiKey
      x-apikeyInfoFunc: openapi_server.controllers.security_controller_.info_from_api_key
```
