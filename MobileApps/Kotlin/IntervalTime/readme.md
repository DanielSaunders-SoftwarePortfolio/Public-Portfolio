# Overview
This is a relatively simple timer app that allows the user to customize an interval length and break length. After the user hits the start button, the counter will then run a timer for the interval length, then immediately switch to the break length, then immediately switch back to the interval etc. This will repeat until the user hits either the stop button or the reset button.

[APP Demo Video](https://youtu.be/FHRFiyMNSB4)

# Development Environment
This app was built in Android Studio using kotlin and typescript. It should run on any android device that is running on android 7.0 or higher.

# Useful Websites
A large majority of the file structure for this app was built automatically by Android Studio's blank project template.
The following two Geeks for Geeks tutorials also contributed to the basic timer functions.
[Geeks for Geeks - Stopwatch tutorial](https://www.geeksforgeeks.org/countdowntimer-in-android-using-kotlin/)
[Geeks for Geeks - Timer tutorial](https://www.geeksforgeeks.org/how-to-create-a-stopwatch-app-using-android-studio/]
I also couldn't have gotten any user input without the help of this site.
[TextChangeListener Code Example](https://kotlincodes.com/kotlin/edittext-text-changelistener-kotlin/)

# Future Work
{Make a list of things that you need to fix, improve, and add in the future.}
* Make Timer run in while the app is in the background
* Add sound notification when timer ends
* Prevent stop button from adding "[Paused]" more than once to the timer label.
