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

def get_user_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input in ['y', 'n']:
            return user_input == 'y'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

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
            # Ignore deleted comments
            if comment.body in ['deleted', '[deleted]', '[removed]']:
                continue

            cleaned_comment = clean_text(comment.body)

            # Remove Edit: part
            if 'Edit:' in cleaned_comment:
                cleaned_comment = cleaned_comment.split('Edit:')[0]

            post_comments.append({
                "Comment": cleaned_comment,
                "Upvotes": comment.score,
                "Comment Author": comment.author.name if comment.author else 'deleted',
                "Comment Posted Time": format_date(comment.created_utc)
            })

        # Build post data
        post_data = {
            "Title": clean_text(post.title),
            "Score": post.score,
            "URL": post.url,
            "Post Author": post.author.name if post.author else 'deleted',
            "Post Date": format_date(post.created_utc),
            "Comments": post_comments
        }

        data.append(post_data)

    return pd.DataFrame(data)


df = scrape_subreddit("AskReddit")

# Save the DataFrame in the 'data' subfolder
df.to_json("data/posts.json", orient="records")

# Open the file and allow the user to select or remove posts
with open('data/posts.json', 'r') as f:
    posts = json.load(f)

kept_posts = []
for post in posts:
    print(f"Post title: {post['Title']}")
    if get_user_input("Keep this post in the JSON? (y/n): "):
        kept_comments = []
        for comment in post['Comments']:
            print(f"Comment: {comment['Comment']}")
            if get_user_input("Keep this comment in the JSON? (y/n): "):
                kept_comments.append(comment)
        post['Comments'] = kept_comments
        kept_posts.append(post)

# Write the kept posts back to the JSON file
with open('data/posts.json', 'w') as f:
    json.dump(kept_posts, f, indent=4)
