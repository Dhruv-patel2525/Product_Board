"""
Each feedback can have votes planning inside
like 
vote -
each feedback can have multiple votes
each vote belong to one feedback

one user can have multiple votes
one vote belong to one user

feedback -> vote One to Many 
user -> vote One to Many
"""
"""
Vote 
id 
feedback_id
user_id
value:[True|False]
created_at
updated_at
unique(feedback_id,user_id)
Index on feedback_id
"""
"""
And also 
for org_level checking need to add org_id right??
foreign_key((feedback_id,org_id))
"""