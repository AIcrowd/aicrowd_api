# AIcrowd API
[![Build Status](https://travis-ci.com/AIcrowd/aicrowd_api.svg?token=thqphyYGsxAAMBx7geLi&branch=master)](https://travis-ci.com/AIcrowd/aicrowd_api)

Python client for server side API of the [aicrowd.com](https://www.aicrowd.com) webapp.

* Free software: GNU General Public License v3
* Documentation: https://aicrowd-api.readthedocs.io.

# Installation
## Deployment
```bash
pip install git+https://github.com/AIcrowd/aicrowd_api.git
```

## Development
```bash
git clone https://github.com/AIcrowd/aicrowd_api
cd aicrowd_api
pip install -r requirements_dev.txt
pip install -e .
```

# Usage
## Instantiate API object
```python
from aicrowd_api import API as AICROWD_API
auth_token="<YOUR AICROWD AUTH TOKEN>"
api = AICROWD_API(auth_token)
```

## Authenticate participant
* with `API_KEY`
```python
api.authenticate_participant(EXAMPLE_API_KEY)
```

* with `username`
```python
api_key = api.authenticate_participant_with_username("spMohanty")
```

## Get all Submissions
```python

challenge_id = "test_challenge"
submissions = api.get_all_submissions(challenge_id)
print(submissions)
```

## Create Submission
```python
challenge_id = "test_challenge"
submission = api.create_submission(challenge_id)
print(submission)

# Output
# ========================================
# AIcrowdSubmission	:	5261
# 	challenge_id	:	test_challenge
# 	round_id	:	False
# 	score	:	False
# 	score_secondary	:	False
# 	grading_status	:	submitted
# 	message	:
# ========================================
```

## Get submission
```python
challenge_id = "test_challenge"
submission_id = 5262
submission = api.get_submission(challenge_id, submission_id)
```

## Update submission
Assuming you have a `submission` object by using `api.create_submission` or `api.get_submission`.
You can update the submission by :

```python
# Update params
submission.grading_status = "graded"
submission.score = 0.98
submission.score_secondary = 0.98
submission.update()
print(submission)
# Output#
# ========================================
# AIcrowdSubmission	:	5262
# 	challenge_id	:	test_challenge
# 	round_id	:	False
# 	score	:	0.98
# 	score_secondary	:	0.98
# 	grading_status	:	graded
# 	message	:
# ========================================
```

# Tests
```bash
# Setup the environment varriables
cp environ.sh.example environ.sh
# Then modify the respective environment variables
source environ.sh
pytests tests/
```

# Author
S.P.Mohanty <mohanty@aicrowd.com>
Arjun Nemani <nemani@aicrowd.com>
