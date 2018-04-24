# crowdAI API
python client for server side API of the [crowdai.org](https://www.crowdai.org) webapp.

* Free software: GNU General Public License v3
* Documentation: https://crowdai-api.readthedocs.io.

# Usage :
* Instantiate API object
```python
from crowdai_api import API as CROWDAI_API
auth_token="<YOUR CROWDAI AUTH TOKEN>"
api = CROWDAI_API(auth_token)
```

## Create Submission
```python
challenge_id = "test_challenge"
submission = api.create_submission(challenge_id)
print(submission)
# Output
# ========================================
# CrowdAISubmission	:	5261
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
submission_id = 5262
challenge_id = "test_challenge"
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
# CrowdAISubmission	:	5262
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
S.P.Mohanty <sharada.mohanty@epfl.ch>
