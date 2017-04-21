# motivation

A system that lets you define re-ocurring "goals" and regularly calculates a "score" for each, based on real time progress "reports". Events occur based on that "score". A "Bank" also exists, which saves up amounts above goal amount, and spends on amounts under the goal.

A "Goal" is configured with the following data:
	-Human readable name
	-Report Identifier
		-Used to match goal with reports
		-Unique
	-"Best case" amount
		-Accumulated target value to hit
		-100% score
	-"Worst case" amount
		-0% score
		-Determines direction (i.e. diet: lower=better, excersize: higher=better)
	-Expected minimum number of reports in time frame
		-Used to detect dis-engagement with reporting, factors into score (worst case assumed)
	-Time frame
		-Range of time used to calculate score, reports older than today-time frame are ignored.
	-Bank amount
		-Starts at 0, added/subtracted from on each evaluation
		-Always at or above 0
		-Unit depens on goal unit
	-Unit type
	
A "Report" consists of:
	-Linked goal
	-Amount field:
		-Generic value, specific to whatever the "Goal" is (minutes for exercize, calories for diet, ect..)
		-Numeric, used for score calculation
	-Timestamp
	-Metadata
		-Text blob, use depends on goal (project name for projects, type of food for diet, ect...)
		-Optional, not used in calculation. More for metrics.
		
The "Score" for each goal is:
	-Ranged between 0-1 (1 being best case)
	-Calculated using formula:
		-Reports within goal time frame are accumulated, as well as counted
		-If accumulated amount is greater than goal, extra is stored in bank. Report amount is then clamped to best case.
		-Else, if amount is under goal, and bank amount exists, subtract difference from bank and apply to amount, up to but not over full bank amount.
		-If amount is under worst case, clip to worst case.
		-Accumulated amount is normalized within "Best case", "Worst case" goal parameters (0-1).
		-If report count is less than min amount allowed, normalize between min amount and 0 (0-1)
		-Subtract count score from amount score and clip to 0-1.
	-Controls severity/amount of events.
	
Components will consist of:
	-Generic DB adaptor, to facilitate swapping between test and prod DB types
	-Score/Bank calculator
	-Events Engine
	
	
Process will run at a set interval, somewhere around 1-15 minutes.
	
