# Tests

## Level of testing

1. **Internal Unit Tests** : _The internal unit tests focus on verifying the internal behavior of a component. These tests are written in the same programming language used to implement the component and involves directly calling functions to assess their functionality._
2. **Component-level Tests** : _Component-level testing involves validating the behavior of a component through its API endpoints to ensure it functions as expected. It focuses on testing the communication between components, often using mocked components to isolate and target specific test scenarios. For the Component-level testing (and later the integration testing) we recommend the Karate tool, to easily automate the testing._
3. **Integration Tests** : _tbd_
4. **Service Chain level Tests** _tbd_

## Testing stages and schedule

### Validation process & tasks

| Stage    | Name     | Description |
| :------- | :------- | :---------- |
| Stage 0  | design document ready |  |
| Stage 1  | BB is running | Building and deploying can be reproduced. Demonstration of working endpoints. In a uniform format |
| Stage 2  | BB is ready to be used in the dataspace   | Internal unit tests reproducible Component-level tests (other components mocked, see sandbox of PDC) |
| Stage 3  | BB can be used in a service chain   | Integration testing with internal dependencies, core components and protocol |
| Stage 4  |  | Integration testing of (partial) service chains. Defined by service chain leaders and BBs |

### Schedule
- Stage 1: Jan 27 ⏳
- Stage 2: Feb 24 ⏳
- Stage 3: March 17
- Stage 4: End of May


## Tests definitions
### Unit Testing

We basically test the 3 steps executed during the Translator processing: 
- rule
- term
- matching

#### Setup test environment
```sh
# Step 1 : Clone the repository
git clone git@github.com:Prometheus-X-association/edge-translators.git

# Step 2 : Navigate to folder
cd edge-translators/

# Step 3 : Handle environment files of each component
cp api/.env.dist api/.env
cp ui/.env.dist ui/.env
cp esco-helper/.env.dist esco-helper/.env

# Step 4 : Start the AI Translator
docker compose up --build
```

#### Run tests
1. `make tests-unit` or `docker compose exec api pytest --no-header --disable-warnings --tb=short -v tests/unit/`

#### Expected results
```bash
user@computer:~/path/to/edge-translators$ make tests-unit 
docker compose exec api uv run pytest --no-header --disable-warnings --tb=short -s -vv tests/unit/
Bytecode compiled 10177 files in 579ms
=============================== test session starts ===============================
collected 35 items                                                                                                                                                           

tests/unit/test_matching_service.py::test_find PASSED
tests/unit/test_matching_service.py::test_find_not_found PASSED
tests/unit/test_matching_service.py::test_update_success PASSED
tests/unit/test_matching_service.py::test_update_exception PASSED
tests/unit/test_matching_service.py::test_find_validated PASSED
tests/unit/test_matching_service.py::test_find_not_validated PASSED
tests/unit/test_matching_service.py::test_find_all PASSED
tests/unit/test_matching_service.py::test_create PASSED
tests/unit/test_matching_service.py::test_delete_success PASSED
tests/unit/test_matching_service.py::test_delete_exception PASSED
tests/unit/test_matching_service.py::test_delete_all_success PASSED
tests/unit/test_matching_service.py::test_delete_all_exception PASSED
tests/unit/test_matching_service.py::test_exists_true PASSED
tests/unit/test_matching_service.py::test_exists_false PASSED
tests/unit/test_matching_service.py::test_set_id PASSED
tests/unit/test_matching_service.py::test_set_object_with_one_validated PASSED
tests/unit/test_matching_service.py::test_set_object_without_validated PASSED
tests/unit/test_matching_service.py::test_generate_new_matching PASSED
tests/unit/test_matching_service.py::test_generate_matching_already_exists PASSED
tests/unit/test_rule_service.py::test_find_success PASSED
tests/unit/test_rule_service.py::test_find_not_found PASSED
tests/unit/test_rule_service.py::test_upsert PASSED
tests/unit/test_rule_service.py::test_delete PASSED
tests/unit/test_rule_service.py::test_browse_rules_tree PASSED
tests/unit/test_rule_service.py::test_display_rules_tree PASSED
tests/unit/test_rule_service.py::test_set_id PASSED
tests/unit/test_rule_service.py::test_generate_id PASSED
tests/unit/test_rule_service.py::test_get_field_name PASSED
tests/unit/test_term_service.py::test_create_collection PASSED
tests/unit/test_term_service.py::test_create_concept PASSED
tests/unit/test_term_service.py::test_delete_concept PASSED
tests/unit/test_term_service.py::test_delete_collection PASSED
tests/unit/test_term_service.py::test_generate[skill_value_to_scale_mapping] PASSED
tests/unit/test_term_service.py::test_generate[polarity_mapping] PASSED
tests/unit/test_term_service.py::test_generate[family_mapping] PASSED

=============================== 35 passed, 8 warnings in 12.08s ===============================
```
### Component Testing

#### 🔐 Auth API Tests
| Test Case ID               | Description                                 | Expected Outcome                                                 | Actual Outcome          | Status  | Notes                           |
|:----------------------------|:--------------------------------------------|:-----------------------------------------------------------------|:------------------------|:--------|:--------------------------------|
| `test_auth_token_success`   | Obtain a token with valid credentials       | 200 OK, token returned with `access_token`, `token_type`, expiry | Matches expected        | Passed  | Mocks successful authentication  |
| `test_auth_token_unauthorized` | Fail to obtain token with invalid credentials | 401 Unauthorized, error `'Unauthorized access'`               | Matches expected        | Passed  | Mocks failed authentication      |

#### 👤 User API Tests
| Test Case ID               | Description                             | Expected Outcome                           | Actual Outcome          | Status  | Notes                                 |
|:----------------------------|:----------------------------------------|:-------------------------------------------|:------------------------|:--------|:--------------------------------------|
| `test_get_me`              | Retrieve current authenticated user     | 200 OK, user info contains `id`             | Matches expected        | Passed  | -                                     |
| `test_get_user`           | Retrieve a user by ID                   | 200 OK, user data matches mocked data       | Matches expected        | Passed  | Mocks `UserRepository.find`           |
| `test_get_user_not_found` | Try to retrieve non-existent user        | 404 Not Found, error `'User not found'`     | Matches expected        | Passed  | Mocks `UserRepository.find` returning `None` |
| `test_get_users`          | Retrieve list of users with pagination   | 200 OK, list of users returned              | Matches expected        | Passed  | Mocks `UserRepository.find_all`       |
| `test_create_user`        | Create a new user                       | 200 OK, created user matches input          | Matches expected        | Passed  | Mocks `UserRepository.create`         |
| `test_update_user`        | Update an existing user’s information    | 200 OK, updated user matches input          | Matches expected        | Passed  | Mocks `UserRepository.find` & `update` |
| `test_delete_user`        | Delete an existing user                 | 200 OK, response is `True`                 | Matches expected        | Passed  | Mocks `UserRepository.find` & `delete` |
| `test_delete_user_not_found` | Attempt to delete non-existent user   | 404 Not Found                              | Matches expected        | Passed  | Mocks `UserRepository.find` returning `None` |

#### ⚙️ Rules API Tests
| Test Case ID             | Description                             | Expected Outcome                         | Actual Outcome          | Status  | Notes                        |
|:--------------------------|:----------------------------------------|:-----------------------------------------|:------------------------|:--------|:-----------------------------|
| `test_get_rules_success`   | Retrieve existing rules               | 200 OK, rules JSON returned              | Matches expected        | Passed  | Mocks ES `get` response      |
| `test_get_rules_not_found` | Try to retrieve rules that don’t exist | 404 Not Found, error `'Missing rules'`   | Matches expected        | Passed  | Mocks ES `get` returning `None` |
| `test_post_rules_success`  | Upsert (post) new rules               | 200 OK, `{ "response": "ok" }`          | Matches expected        | Passed  | Mocks ES `upsert`            |
| `test_post_rules_invalid`  | Submit invalid (empty) rules          | 422 Unprocessable Entity                 | Matches expected        | Passed  | Validates request body       |

#### 📄 Transform API Tests
| Test Case ID                     | Description                                    | Expected Outcome                                 | Actual Outcome          | Status  | Notes                                  |
|:----------------------------------|:-----------------------------------------------|:-------------------------------------------------|:------------------------|:--------|:---------------------------------------|
| `test_transform_success`          | Transform a valid document                     | 200 OK, response matches expected output         | Matches expected        | Passed  | Mocks multiple ES `search/get` requests |
| `test_transform_invalid_document` | Submit invalid (empty) document                | 422 Unprocessable Entity                        | Matches expected        | Passed  | Validates request body                 |
| `test_transform_missing_document` | Submit request without `document` field        | 422 Unprocessable Entity                        | Matches expected        | Passed  | Validates required fields             |
| `test_transform_rules_not_found`  | Try transforming when rules are missing        | 404 Not Found, error `'Missing rules'`          | Matches expected        | Passed  | Mocks missing ES rules                |

#### 🔄 Matching API Tests
| Test Case ID                               | Description                                    | Expected Outcome                                 | Actual Outcome          | Status  | Notes                                 |
|:--------------------------------------------|:-----------------------------------------------|:-------------------------------------------------|:------------------------|:--------|:--------------------------------------|
| `test_get_matching_experience_validated_true`  | Retrieve validated experiences from ES        | 200 OK, list of experiences returned             | Matches expected        | Passed  | Mocks ES search with validated experiences |
| `test_get_matching_experience_validated_false` | Retrieve non-validated experiences from ES    | 200 OK, list of experiences returned             | Matches expected        | Passed  | Mocks ES search with non-validated experiences |
| `test_get_matching_skill_validated_false`      | Retrieve non-validated skills from ES         | 200 OK, list of skills returned                 | Matches expected        | Passed  | Mocks ES search with non-validated skills |

#### Setup test environment
```sh
# Step 1 : Clone the repository
git clone git@github.com:Prometheus-X-association/edge-translators.git

# Step 2 : Navigate to folder
cd edge-translators/

# Step 3 : Handle environment files of each component
cp api/.env.dist api/.env
cp ui/.env.dist ui/.env
cp esco-helper/.env.dist esco-helper/.env

# Step 4 : Start the AI Translator
docker compose up --build
```

#### Run tests
1. `make tests-api` or `docker compose exec api pytest --no-header --disable-warnings --tb=short -v tests/api/`

#### Expected results

```bash
make tests-api
docker compose exec api uv run pytest --no-header --disable-warnings --tb=short -s -v tests/api/
Bytecode compiled 10177 files in 536ms
=============================== test session starts ===============================
collected 21  items                                                                                                                                                           

tests/api/auth/test_auth.py::test_auth_token_success PASSED
tests/api/auth/test_auth.py::test_auth_token_unauthorized PASSED
tests/api/matching/test_matchings.py::test_get_matching_experience_validated_true PASSED
tests/api/matching/test_matchings.py::test_get_matching_experience_validated_false PASSED
tests/api/matching/test_matchings.py::test_get_matching_skill_validated_false PASSED
tests/api/rules/test_rules.py::test_get_rules_success PASSED
tests/api/rules/test_rules.py::test_get_rules_not_found PASSED
tests/api/rules/test_rules.py::test_post_rules_success PASSED
tests/api/rules/test_rules.py::test_post_rules_invalid PASSED
tests/api/transform/test_transform.py::test_transform_success PASSED
tests/api/transform/test_transform.py::test_transform_invalid_document PASSED
tests/api/transform/test_transform.py::test_transform_missing_document PASSED
tests/api/transform/test_transform.py::test_transform_rules_not_found PASSED
tests/api/users/test_users.py::test_get_me PASSED
tests/api/users/test_users.py::test_get_user PASSED
tests/api/users/test_users.py::test_get_user_not_found PASSED
tests/api/users/test_users.py::test_get_users PASSED
tests/api/users/test_users.py::test_create_user PASSED
tests/api/users/test_users.py::test_update_user PASSED
tests/api/users/test_users.py::test_delete_user PASSED
tests/api/users/test_users.py::test_delete_user_not_found PASSED

=============================== 21 passed, 56 warnings in 36.60s ===============================
```