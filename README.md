# amazon-connect-cloud-contact-center
Implementation and Optimization of Amazon Connect Cloud Contact Center with sample contact flows and Lambda integration.

This repository contains the complete implementation of a cloud‑based contact center using Amazon Connect, AWS Lambda, and an external real-time Bus Arrival API. The system was designed to support:
- IVR for bus arrival information
- Real-time ETA lookup using Lambda
- Language-based queue routing (English / Hindi)
- Agent escalation
- Hours-of-Operation handling
- Clear error handling and retry logic

# Project Overview
This project delivers a production-style serverless contact center using Amazon Connect. The finalized implementation supports:
- A Welcome + Main Menu
- DTMF-based user inputs for Bus Stop Code & Service Number
- Connection to AWS Lambda for real-time bus arrival information
- A Post-response menu to continue, restart, or escalate
- Agent transfer with language-based routing
- Hours-of-Operation validation
- Dedicated prompts and retry logic

# System Architecture
High-Level Call Flow
1. Caller dials Connect number
2. Welcome & Main Menu
3. Hours-of-Operation Check
4. Language Selection
5. DTMF Capture
   - Bus Stop Code (5 digits)
   - Service Number
6. Lambda Invocation → External Bus Arrival API
7. Lambda returns human-friendly FinalArivalTime string
8. System plays ETA message
9. Post-response Menu:
    - Check again
    - Main menu
    - Connect to Agent
10. Queue Routing (English/Hindi)
11. Agent handles call

# Prerequisites
1. AWS Account
2. Amazon Connect Instance (Telephony Enabled)
3. IAM Permissions for:
   - Lambda
   - Connect
   - CloudWatch Logs
4. LTA DataMall API key
5. Phone number claimed in Amazon Connect

# End-to-End Deployment Guide
Follow this guide step-by-step to deploy the entire system from scratch.

**Step 1 — Deploy AWS Lambda**
1.1 Create the Function
	Go to AWS Lambda → Create Function
	Runtime: Python 3.12
	Name: DemoBusSupport
1.2 Add Code
	Use the provided lambda/lambda_function.py (from this repo).
1.3 Add Environment Variable
	ACCOUNTKEY=<your LTA API key>

**Step 2 — Import Contact Flow into Amazon Connect**
2.1 Go to: Amazon Connect Console → Routing → Contact Flows
2.2 Choose "Create → Import Flow"
	Upload:
	contact-flows/Demo Bus Support.json

2.3 Update the following Inside the Flow
	Lambda Block
		Choose your Lambda → DemoBusSupport
		The flow passes attributes:
		JSON{  "BusStopCode": "$.Attributes.BusStopCode",  "ServiceNo": "$.Attributes.ServiceNo"}Show more lines

	Queue Blocks
		Update:
		“Set queue for English”
		“Set queue for Hindi”
		With real queue ARNs in your instance.

	Hours-of-Operation Block
		Choose your Connect’s Hours resource.

2.4 Publish the Flow

**Step 3 — Configure Queues & Routing**
3.1 Create Queues
	Demo Bus Support – English
	Demo Bus Support – Hindi

3.2 Assign Queues to Routing Profiles
	Agents must belong to a routing profile pointing to these queues.

3.3 Agent Setup
	Add agents under:
	Users → User Management

**Step 4 — Assign Contact Flow to Phone Number**
4.1 Go to Routing → Phone Numbers
4.2 Choose or claim a number
4.3 Set Inbound Flow to:
		Demo Bus Support
Now the line is live.

# Testing Guide
1. Call the Amazon Connect number
2. Hear Welcome Menu
3. Press 1 → Bus Arrival workflow
4. Enter Bus Stop Code → hear confirmation
5. Enter Service Number → confirmation
6. Wait for ETA from Lambda (e.g., “Arriving in 3 minutes and 22 seconds”)
7. Post-response menu appears
8. Press 3 → agent escalation
9. Language Selection occurs
10. Connect routes to correct queue

