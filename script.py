# Code adapted from https://github.com/kelseyywang/reddit-notifs
# https://www.freecodecamp.org/news/make-a-custom-reddit-notification-system-with-python-4dd560667b35/
import time
import praw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from praw.models import MoreComments
from datetime import datetime
from constants import (
    SUBREDDIT,
    NUM_POSTS,
    KEYWORD_GROUPS,
    SLEEP_TIMER,
)

import secrets


class RedditNotifications:
    def __init__(self):
        self.processed = []
        self.reddit = self.auth()

    def check_posts(self):
        print(f"Checking Reddit posts @ {str(datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))} ...")
        if matching_posts := self.get_posts():
            content = ""
            for keyword_count, post in matching_posts:
                # Append info for this relevant post to the email content
                content += f"""
                    {post['created']} | {post['flair']}
                    <br />
                    {post['title']}
                    <br><br>
                    Comments ({post['comment_count']}):<br>
                    {post['comments']}<br>
                    {post['url']}
                    <br><br>
                    <hr><br>
                """
            if len(matching_posts) > 0:
                print(f"{len(matching_posts)} Matching post(s) found, sending email")
                RedditNotifications.send_email(content)

    def get_posts(self):
        """ Returns tuples containing keyword count & post info dict of matching posts """

        # Designate subreddit to explore
        subreddit = self.reddit.subreddit(SUBREDDIT)
        matching_posts = []
        # Explore new posts in subreddit
        for submission in subreddit.new(limit=NUM_POSTS):
            if submission.id in self.processed:
                pass
            title = submission.title
            for keywords in KEYWORD_GROUPS:
                keyword_count = RedditNotifications.get_keyword_count(title.lower(), keywords)
                if keyword_count != -1:
                    comment_count = len(list(submission.comments))
                    if submission.id not in self.processed and comment_count >= 2:
                        comments = []
                        for comment in submission.comments:
                            if isinstance(comment, MoreComments):
                                continue
                            comment_html = f"""
                            {comment.author} ({comment.author_flair_text}) | 
                            {datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')}
                            <br>
                            {comment.body_html}
                            <br>
                            =======
                            <br>
                            """
                            comments.append(comment_html)
                        post_dict = {
                            "id": submission.id,
                            "title": title,
                            "created": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                            "flair": submission.link_flair_text,
                            "keyword_count": keyword_count,
                            "url": f"https://www.reddit.com{submission.permalink}",
                            "comment_count": comment_count,
                            "comments": ''.join(comments),
                        }
                        self.processed.append(submission.id)
                        matching_posts.append((keyword_count, post_dict))
        # Sort asc by the keyword count
        matching_posts.sort(key=lambda x: x[0])
        return matching_posts

    @staticmethod
    def auth():
        return praw.Reddit(
            client_id=secrets.MY_CLIENT_ID,
            client_secret=secrets.MY_CLIENT_SECRET,
            user_agent=secrets.MY_USER_AGENT,
            username=secrets.MY_REDDIT_USERNAME,
            password=secrets.MY_REDDIT_PASSWORD,
        )

    @staticmethod
    def get_keyword_count(search, keywords):
        """Returns a count of secondary terms if is relevant, -1 otherwise"""

        keyword_count = 0
        # required, secondary, min_secondary = KEYWORDS_GROUP
        required, secondary, min_secondary = keywords
        for required_term in required:
            if required_term not in search:
                return -1
        for secondary_term in secondary:
            if secondary_term in search:
                # A secondary term was found, so add to keyword_count
                keyword_count += 1
        if keyword_count < min_secondary:
            return -1
        return keyword_count

    @staticmethod
    def send_email(content):
        email_list = [
            secrets.RECEIVER_EMAIL
            # Add any other email addresses to send to
        ]
        subject = f"New `r/{SUBREDDIT}` posts @ {str(datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))}"
        server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(secrets.SENDER_EMAIL, secrets.SENDER_PASSWORD)
        for email_address in email_list:
            # Send emails in multiple part messages
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = secrets.SENDER_EMAIL
            msg["To"] = email_address
            # HTML of email content
            html = f"<html><head></head><body>{content}</body></html>"
            msg.attach(MIMEText(html, "html"))
            server.sendmail(secrets.SENDER_EMAIL, email_address, msg.as_string())
        server.quit()


if __name__ == "__main__":
    start_time = time.time()
    reddit = RedditNotifications()

    while True:
        try:
            reddit.check_posts()
        except Exception as e:
            print(e)
            continue
        time.sleep(SLEEP_TIMER - ((time.time() - start_time) % SLEEP_TIMER))
