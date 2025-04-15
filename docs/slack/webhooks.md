# Sending Messages with Webhooks

Incoming webhooks are a simple way to post messages from apps into Slack. When you create an incoming webhook, Slack provides a unique URL to which you send a JSON payload containing the message and formatting options. These webhooks support all standard formatting and layout blocks for rich message content.

### 1. Create a Slack App

First, [create a Slack app](https://api.slack.com/apps):

- Choose a name for your app.
- Associate it with a Slack workspace.
- Optionally, create a dedicated channel for testing.

Once your app is created, you'll be redirected to its settings page.

### 2. Enable Incoming Webhooks

From your app's settings:

- Select **Incoming Webhooks** from the sidebar.
- Toggle the **Activate Incoming Webhooks** option to `on`.

Manage existing apps:
[App Management Dashboard](https://api.slack.com/apps)

### 3. Create an Incoming Webhook

With webhooks enabled, new options appear:

- Click the **Add New Webhook to Workspace** button.
- Choose a channel for the webhook to post to.
- Click **Authorize**.

Slack will redirect you back to the app settings, where a webhook URL will now appear under **Webhook URLs for Your Workspace**.

Example URL:

``` http
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

This URL is specific to your app and the channel you selected.

!!! danger
    **Do not share** your webhook URL publicly. It is a secret and can be used to post to your Slack workspace.

### 4. Send a Message

To post a message using your webhook, make an HTTP POST request with a JSON body.

Example:

``` http
POST https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
Content-type: application/json

{
    "text": "Hello, world."
}
```

---

Reference: :material-slack:{ style="color:#7c0480" } [Slack Webhooks](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks)

---
