#the selenium URL Loader is going to prove difficult, I'm just going to scrape the top posts using plain selenium
#get it done over getting it perfect
import praw
import json
import os 
import pandas as pd

 

reddit = praw.Reddit(
    client_id="FMgswHRMtITBLNDWhd-_Wg",
    client_secret="GPZSEHHfYWZE2nIdMDDzCQye3PIsqA",
    user_agent="No_Concert1617"
)



def scrape_subreddit(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    data = []

    top_posts = subreddit.top(limit=10)
    for post in top_posts:
        post.comments.replace_more(limit=0)
        
        # Sort the top-level comments by score in descending order
        sorted_comments = sorted(post.comments, key=lambda x: x.score, reverse=True)

        post_comments = []
        for comment in sorted_comments[:10]:
            post_comments.append({
                "Comment": comment.body,
                "Upvotes": comment.score
            })

        data.append({
            "Title": post.title,
            "Score": post.score,
            "URL": post.url,
            "Comments": post_comments
        })

    return pd.DataFrame(data)

df = scrape_subreddit("AskReddit")

# Create 'data' subfolder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Save the DataFrame in the 'data' subfolder
df.to_json("data/posts.json", orient="records")

# Print the contents of the file
with open('data/posts.json', 'r') as f:
    print(json.dumps(json.load(f), indent=4))

