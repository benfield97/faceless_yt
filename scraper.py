import praw
import json
import os 
import pandas as pd
import unicodedata
import datetime

reddit = praw.Reddit(
    client_id="FMgswHRMtITBLNDWhd-_Wg",
    client_secret="GPZSEHHfYWZE2nIdMDDzCQye3PIsqA",
    user_agent="No_Concert1617"
)

def clean_text(text):
    # Remove newline characters and normalize the text
    text = text.replace('\n', ' ')
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()

def format_date(created_utc):
    post_date = datetime.datetime.fromtimestamp(created_utc)
    now = datetime.datetime.now()
    difference = now - post_date

    if difference.days > 365:
        years = difference.days // 365
        return f"{years} year ago" if years == 1 else f"{years} years ago"
    else:
        return f"{difference.days} day ago" if difference.days == 1 else f"{difference.days} days ago"

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
            cleaned_comment = clean_text(comment.body)
            post_comments.append({
                "Comment": cleaned_comment,
                "Upvotes": comment.score,
                "Comment Author": comment.author.name if comment.author else 'deleted',
                "Comment Posted Time": format_date(comment.created_utc)
            })

        data.append({
            "Title": clean_text(post.title),
            "Score": post.score,
            "URL": post.url,
            "Post Author": post.author.name if post.author else 'deleted',
            "Post Date": format_date(post.created_utc),
            "Comments": post_comments
        })

    return pd.DataFrame(data)


df = scrape_subreddit("AskReddit")

# Create 'data' subfolder if it doesn't exist
if not os.path.exists('faceless_yt/data'):
    os.makedirs('data')

# Save the DataFrame in the 'data' subfolder
df.to_json("faceless_yt/data/posts.json", orient="records")

# Print the contents of the file
with open('faceless_yt/data/posts.json', 'r') as f:
    print(json.dumps(json.load(f), indent=4))
