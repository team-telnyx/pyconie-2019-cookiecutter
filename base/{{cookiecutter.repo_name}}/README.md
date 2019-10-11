
# {{cookiecutter.app_name}}


{{cookiecutter.project_short_description}}

---

# Welcome to the PyConIE 2019 aiohttp Workshop!

In this workshop we'll be going over the high levels of what asynchronous code is and we'll be taking a close look at two libraries: asyncio which comes with the Python standard library, and aiohttp which is built on top of asyncio.

We'll also be building a simple web server that will interface with a 3rd party API that will allow us to make real phone calls right from our server.

We'll discuss some benefits of using asynchronous code and some of the common pitfalls when changing over your synchronous code to asynchronous.

Let's get started!

## Section 1: Getting Setup
We need to make sure that your local environment is setup properly for you to follow along in this workshop.

First of all we need a few python packages to get started. We also need to make sure you're running a compatible version of Python. This workshop assumes you're running > Python 3.5.2.

Run the following:
```python
python3 setup/confirm_environment.py
```

If everything is correctly installed and confirmed you should see this in your terminal:
```
Success! Your local environment is setup correctly and you're ready for this workshop!
```

Setup your virual environment with the following:
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Section 2: Setting up our Accounts
### Setting up ngrok
1. Open up a new terminal
2. visit [ngrok](https://ngrok.com)
3. Click `Get started for free`
4. Create your account
5. Download ngrok for your machine
6. Follow your OS instructions to get started
7. Run the server `./ngrok http 8080`
8. Copy the forwarding domain in your terminal window (keep this terminal window open)
9. Ensure it's working correctly by copying the domain in your browswer and ensuring that you see a `502 Bad Gateway` error in your ngrok terminal screen
10. Keep your terminal window open to keep your ngrok tunnel open
> You'll get a 502 error because our service isn't listening for traffic yet.

### Setting up Telnyx
1. Visit [Telnyx](https://portal.telnyx.com)
2. Sign in using the account information given to you
3. Visit the `Connections` tab on the left
4. Edit the `PyConIE 2019 Workshop` connection
5. Copy the `Connection ID` and save it somewhere for now
6. Update the `Webhook URL` with your ngrok public domain
> Be sure to include /webhook in your webhook url address to ensure the Telnyx Webhooks get routed to the correct handler
7. Confirm that your account is setup for API v2 webhooks
8. Click `Set Call Control Auth` and click `Save All Changes`
9. Visit the `Auth` tab on the left
10. Ensure you're on `API V2` and create a new api key
11. Save the API key somewhere for now
12. Visit the `Numbers` tab on the left
13. Find the number on your account and copy it and save it somewhere


## Section 3: Let's start diving into asyncio

We'll start off by diving into asyncio.
```python
cd setup/
python3 asyncio_example.py
```

Open up the folder and take a look at the file. This is a simple script to help break down what asynchronous is and how it works. Let's take a look at `main()` and `__main__`.

### \_\_main\_\_
The first thing we're doing is setting up the asyncio event loop.
Then we're calling  `main()` to run until it's complete inside the loop. Notice how we don't have `await` anything at this point. That's ok because `loop.run_until_complete()` takes a coroutine as an argument.

### main()
First we're printing `coro_test()` without an `await`. This leaves it as a coroutine and when we print it we get something like this:
```bash
<coroutine object coro_test at 0x7fac4ef4f410>
```
Now the next line we're doing the same thing but we `await` it and there we can see that the function was called and executed and it prints out:
```bash
this is a coroutine
```

Next we're calling and awaiting `asyncio.gather()`. This takes in multiple coroutines as the argument and runs them together making the most use of the asynchronous behavior of each coroutine. It does the awaiting automatically. If you have anything being returned, you can capture them as normal still here.

In our case, we're calling 4 simulated "heavy" tasks. Each heavy task is just a simple sleep statement. They all sleep for different amounts of time. But we'll see that they always finish within 7 seconds and not 13 seconds.

This is because when the first task sleeps, it releases control back to the event loop. The event loop then gives the processing time to the next task and does the same thing. Once `heavy_task_4` has finished it's work (sleeping) it makes a call back to the event loop which gives it control again to finish the next task. It keeps working like that until everything is completed.


## Section 4: Next up is aiohttp

Let's take a look at aiohttp now. We'll start off with the client side of things.

Open up `aiohttp_example.py` and take a look around. This example opens up 4 different websites asynchronously, writes the html response to a file and logs the time to fetch each website's response.

Go ahead and run the file and note the output:
```python
python3 aiohttp_example.py
```
Things to note here is that the total time to fetch and process each site individually is less than the total runtime of the script. Recall that this is possible because once we make the request to the first site, there's wait time on our end while the remote server processes the request and sends the content back to us. While we're waiting for the response, instead of locking the I/O thread, the event loop moves on to the next task that's ready to process. This repeats until the response is received from any of the websites at which time the event loop makes time for the task to pickup where it left off and finished it's job.


## Section 5: **Dial-A-Joke**
Now we'll jump to using aiohttp-server. There's a fair amount of boilerplate we've already gone ahead and created to save time and headache here. We'll be going through the code in a live walkthrough. But there's some high level information here as well.

### File Structure OVerview

#### dialajoke
The application and all it’s files.

#### server
Contains the logic to setup and configure our actual server. This includes server port configurations and CORS settings, as well as setting up routes and their handlers.

#### templates
Holds the html files that will be rendered and served to allow the user to schedule a call

#### config.dev.json
Where you can easily set and modify your environment variables

#### tests
This holds our unit test files

#### Makefile and  tasks
Holds information so we can use invoke to easily run our app

### Functionality Overview
Everything for this service is handled inside `infrastructure` directory.

`server` - contains all of the HTTP handlers as well as the setup configurations for our server
`call_control.py` - contains the CallControl class which handles processing webhooks and firing off the call related API requests
`scheduler.py` - contains the UnifiedTimedQueue class which is in charge of maintaining scheduled calls and firing them off when it’s time
`usecases.py` - contains parsing logic
`validators.py` - contains logic to validate the input data

### Next Steps: Process the Webhook as a background task

Why is this important?

Normally, you’d have more processing to do than just this. You may be making an API call to another service to get some more information, or you may make a DB request and need to parse the response.

This takes time, and the webhook server is expecting a response back. If you take too long, it may resend the webhook or do something else that causes unintended events.
To mitigate this, you can do the processing as a task.

When you create a task in the aiohttp framework, it runs “behind the scenes” and allows you to continue processing without being bogged down.



> [https://docs.python.org/3.6/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.create_task](https://docs.python.org/3.6/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.create_task)


### Next Steps: Write Unit Tests

Why is this important?

Unit tests are vital to good code practice. They allow us to find potential bugs and fix them before they get shipped to prod.

Good unit tests allow developers to be confident that their changes aren’t breaking other parts of the code.

We’ve created a boilerplate framework as a reference point. Expand upon it and ensure you're testing everything thoroughly.

 > [https://aiohttp.readthedocs.io/en/stable/testing.html#pytest-example](https://aiohttp.readthedocs.io/en/stable/testing.html#pytest-example)


### Next Steps: Add Custom Middleware

Why do we need this?

Custom middle provides a lot of benefits:

1.  You can add metrics handling directly to new routes. It helps keep your code DRY.

2.  Add custom exception handling. Also helps keep your code DRY.

3.  Allow conformity when different developers are working on the same codebase.

Add some custom middleware to do some basic exception handling.
Format the errors to be in a standardized schema.

> [https://docs.aiohttp.org/en/stable/web_advanced.html#middlewares](https://docs.aiohttp.org/en/stable/web_advanced.html#middlewares)





This project was brought to you by: [Telnyx PyCon IE 2019 Cookiecutter Template](https://github.com/team-telnyx/pyconie-2019-cookiecutter)
