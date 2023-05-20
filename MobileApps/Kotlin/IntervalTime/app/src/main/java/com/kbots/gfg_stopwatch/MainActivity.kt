package com.kbots.gfg_stopwatch

import android.app.Activity
import android.os.Bundle
import android.os.Handler
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.EditText
import android.widget.TextView
import java.util.Locale


class MainActivity : Activity() {
    // Use seconds, running and wasRunning respectively
    // to record the number of seconds passed,
    // whether the stopwatch is running and
    // whether the stopwatch was running
    // before the activity was paused.
    // Number of seconds displayed
    // on the stopwatch.
    private var secondsInInterval = 0
    private var secondsInBreak = 0
    private var seconds = 0
    private var onBreak = false
    private var running = false
    private var wasRunning = false
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        var editInterval = findViewById<View>(
            R.id.edit_interval
        ) as EditText
        var editBreak = findViewById<View>(
            R.id.edit_break
        ) as EditText
        secondsInInterval = editInterval.text.toString().toInt()
        secondsInBreak = editBreak.text.toString().toInt()

        editInterval.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable?) {

            }

            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {
            }

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                if (s != null) {
                    if (s.isNotEmpty())
                        secondsInInterval = s.toString().toInt()
                }
            }
        })
        editBreak.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable?) {
            }

            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {
            }

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                if (s != null) {
                    if (s.isNotEmpty())
                        secondsInBreak = s.toString().toInt()
                }
            }
        })

        val timerName = findViewById<View>(
            R.id.interval_name
        ) as TextView
        timerName.text = ""

        if (savedInstanceState != null) {

            // Get the previous state of the stopwatch
            // if the activity has been
            // destroyed and recreated.
            seconds = savedInstanceState
                .getInt("seconds")
            running = savedInstanceState
                .getBoolean("running")
            wasRunning = savedInstanceState
                .getBoolean("wasRunning")
        }
        runTimer()
    }

    // Save the state of the stopwatch
    // if it's about to be destroyed.
    public override fun onSaveInstanceState(
        savedInstanceState: Bundle
    ) {
        savedInstanceState
            .putInt("seconds", seconds)
        savedInstanceState
            .putBoolean("running", running)
        savedInstanceState
            .putBoolean("wasRunning", wasRunning)
    }

    // If the activity is paused,
    // stop the stopwatch.
    override fun onPause() {
        super.onPause()
        wasRunning = running
        running = false
        val timerName = findViewById<View>(
            R.id.interval_name
        ) as TextView
        timerName.text = timerName.text.toString() + " [Paused]"
    }

    // If the activity is resumed,
    // start the stopwatch
    // again if it was running previously.
    override fun onResume() {
        super.onResume()
        if (wasRunning) {
            running = true
        }
    }

    // Start the stopwatch running
    // when the Start button is clicked.
    // Below method gets called
    // when the Start button is clicked.
    fun onClickStart(view: View?) {
        running = true
        wasRunning = true
        val timerName = findViewById<View>(
            R.id.interval_name
        ) as TextView
        if (!onBreak) {
            timerName.text = "Workout!"
        } else {
            timerName.text = "Rest"
        }
    }

    // Stop the stopwatch running
    // when the Stop button is clicked.
    // Below method gets called
    // when the Stop button is clicked.
    fun onClickStop(view: View?) {
        running = false
        val timerName = findViewById<View>(
            R.id.interval_name
        ) as TextView

        timerName.text = if (wasRunning) {timerName.text.toString() + " [Paused]"} else {""}
    }

    // Reset the stopwatch when
    // the Reset button is clicked.
    // Below method gets called
    // when the Reset button is clicked.
    fun onClickReset(view: View?) {
        running = false
        wasRunning = false
        seconds = 0
        onBreak = false
        val timerName = findViewById<View>(
            R.id.interval_name
        ) as TextView
        timerName.text = ""
    }

    // Sets the NUmber of seconds on the timer.
    // The runTimer() method uses a Handler
    // to increment the seconds and
    // update the text view.
    private fun runTimer() {

        // Get the text view.
        val timeView = findViewById<View>(
            R.id.time_view
        ) as TextView

        // Creates a new Handler
        val handler = Handler()

        // Call the post() method,
        // passing in a new Runnable.
        // The post() method processes
        // code without a delay,
        // so the code in the Runnable
        // will run almost immediately.
        handler.post(object : Runnable {
            override fun run() {
                var secondsInCurrent = if (!onBreak) {
                    secondsInInterval
                } else {
                    secondsInBreak
                }
                val minutes = (secondsInCurrent-seconds)/60
                val secs = (secondsInCurrent-seconds)%60


                // Format the seconds into hours, minutes,
                // and seconds.
                val time = String.format(
                    Locale.getDefault(),
                    "%02d:%02d", minutes, secs
                )

                // Set the text view text.
                timeView.text = time

                // If running is true, increment the
                // seconds variable.
                if (running) {
                    seconds++
                    if (seconds > secondsInCurrent) {
                        onBreak = !onBreak
                        seconds = 0
                        val timerName = findViewById<View>(
                            R.id.interval_name
                        ) as TextView
                        if (!onBreak) {
                            timerName.text = "Workout!"
                        } else {
                            timerName.text = "Rest"
                        }
                    }
                }

                // Post the code again
                // with a delay of 1 second.
                handler.postDelayed(this, 1000)
            }
        })
    }
}