# Scenario

:::image type="content" source="images/contoso-outdoors-product-page.png" alt-text="A screenshot of the Contoso Outdoor Gear product page for the Contoso Tent.":::

Contoso Outdoor Gear would like to apply content moderation to their customer review feature on their website.

:::image type="content" source="images/contoso-outdoors-customer-feedback.png" alt-text="A screenshot of the customer review feature on the Contoso Outdoor Gear e-commerce site.":::

## Prerequisites

Running the demo requires the following:
- [Visual Studio Code](https://code.visualstudio.com/Download)
- A [Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/overview) resource deployed in a [supported region](https://learn.microsoft.com/azure/ai-services/content-safety/overview#region-availability)
    - Once deployed, locate the resource **key** and **endpoint** within **Resource Management** > **Keys and Endpoint**

## How to start the sample

1. Download or fork the [RAI Workshops](https://www.github.com/azure-samples/RAI-workshops) repository.
    1. Download:
    1. Fork:
1. Open the repository files or the fork inside Visual Studio Code.
1. Create a `.env` file and add an entry for the following environment variables:
    1. `CONTENT_SAFETY_KEY=<Your Content Safety Key>`
    1. `CONTENT_SAFETY_ENDPOINT="<Your Content Safety Endpoint>"`
1. Create a virtual environment.
1. Open the terminal and enter the command `pip install -r requirements.txt`.
1. In the terminal, navigate into myproject with the command: `cd myproject`.
1. In the terminal, run the command: `python manage.py runserver`
1. Click the link in the terminal to view the webpage locally.

## How to demo the sample

You can enter a comment into the **Text** box and press **Submit Review** to post. If the comment is safe (i.e. the comment is not triggered by the text moderation system), the comment will post. However, if the comment is harmful (i.e. it triggers at least one of the [harm categories](https://aka.ms/harm-categories)), a message displays indicating that the content is not allowed.

## How to remove comments

Comments are stored locally within the project database. You can remove the comments in the sample via the Django Shell by running the following commands in the terminal:

1. Open the Django shell: `python manage.py shell`
1. Import the Comment model: `from myapp.models import Comment`
1. Delete all comments: `Comment.objects.all().delete()`
1. Exit the shell: `exit()`

## How to modify the sample

This sample is created within a [Django](https://www.djangoproject.com/) project. If you're unfamiliar with Django, it's recommended to review the Django [documentation](https://docs.djangoproject.com/5.1/).

The `moderate_content.py` file contains the logic for the moderation system. You can customize both the conditional logic and output text for the text moderation feature wihtin lines 39 - 49.