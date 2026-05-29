# QR Code Tools Management System — User Guide

---

## Table of Contents

1. [What Is This System?](#1-what-is-this-system)
2. [Getting Started — Logging In](#2-getting-started--logging-in)
3. [Understanding User Roles](#3-understanding-user-roles)
4. [Admin Guide](#4-admin-guide)
   - [Tool Master — Managing Tools](#41-tool-master--managing-tools)
   - [Dashboard — Overview & Charts](#42-dashboard--overview--charts)
   - [Reports](#43-reports)
   - [Alerts](#44-alerts)
   - [Users Management](#45-users-management)
5. [Inspector Guide](#5-inspector-guide)
6. [Store Manager Guide](#6-store-manager-guide)
7. [Worker Guide](#7-worker-guide)
8. [Management Guide](#8-management-guide)
9. [Data Entry Guide](#9-data-entry-guide)
10. [Split Tool Matching](#10-split-tool-matching)
11. [Bulk Import Tools](#11-bulk-import-tools)
12. [QR Codes Explained](#12-qr-codes-explained)
13. [Alerts Explained](#13-alerts-explained)
14. [Frequently Asked Questions](#14-frequently-asked-questions)

---

## 1. What Is This System?

The **QR Code Tools Management System** is a digital platform for tracking construction and industrial tools across multiple job sites. It replaces manual paper logs with a smart, scannable system.

**What you can do with it:**

| Capability | Description |
|---|---|
| Track tools | Know where every tool is, its condition, and who last used it |
| Scan QR codes | Instantly pull up any tool's details by scanning its QR sticker |
| Run inspections | Record safety checks with photos and usability ratings |
| Move tools | Log when tools move between sites and subcontractors |
| Get alerts | Automatic warnings for expired or damaged tools |
| Generate reports | Export tool lists and certificates as Excel or PDF |
| Match split tools | Verify that Part A and Part B of a tool belong together |

---

## 2. Getting Started — Logging In

1. Open your browser and navigate to the system URL (e.g., `http://192.168.x.x:5173`).
2. You will see the **Login** screen.
3. Enter your **username** and **password**.
4. Click **Sign In**.

> **Tip:** You can also log in by **scanning your own QR code** if your admin has set one up for you.

If you don't have login credentials, contact your system administrator.

---

## 3. Understanding User Roles

Each person has a role that controls what they can see and do.

| Role | What They Can Do |
|---|---|
| **Admin** | Full access — create/edit/delete tools, manage users, view all pages |
| **Data Entry** | Create and import tools at their assigned site |
| **Inspector** | Scan tools and record safety inspection results |
| **Store Manager** | Manage tool transactions (in/out) at their store location |
| **Worker** | Scan tools to view information (read-only) |
| **Management** | View dashboard, reports, and alerts (no editing) |

After logging in, you will automatically be taken to the page that matches your role.

---

## 4. Admin Guide

Admins have access to all pages via the left-side navigation menu.

---

### 4.1 Tool Master — Managing Tools

**Location:** Sidebar → Tool Master

This is where all tools are created, viewed, and edited.

The page has three tabs:

#### Tab 1 — New Entry (Create a Tool)

Fill in the form fields:

| Field | What to Enter |
|---|---|
| **Description** | Name of the tool (e.g., "Clamp Head") |
| **Make / Year** | Manufacturer or year of manufacture |
| **Capacity** | Load capacity (e.g., "8 Ton") |
| **Safe Working Load (SWL)** | Maximum safe load |
| **Tool Type** | Erection Tools or Stringing Tools |
| **Metal Type** | Material the tool is made from |
| **Tool Variant** | Specific variant/model |
| **Purchaser Name & Contact** | Who purchased the tool |
| **Supplier Code** | Supplier reference |
| **Date of Supply** | When the tool was received |
| **Validity Period** | How many years the tool is certified for |
| **Test Certificate** | Upload the PDF/image certificate |
| **Current Site** | Where the tool is located now |
| **Subcontractor Details** | Name, code, and mobile of the subcontractor (if applicable) |
| **Job Code / Description** | Project reference |
| **Remarks** | Any additional notes |

Click **Save Tool**. The system will automatically generate a unique **QR code** for this tool.

---

#### Tab 2 — Saved Tools (View & Edit)

- A table lists all tools in the system.
- Use the **search bar** to find tools by any field.
- Filter by **site** or **creator** using the dropdowns.
- Click a tool row to **view full details**.
- Click the **Edit** icon to update tool information.
- Click the **QR icon** to view and print the tool's QR code.

> **Note:** Every time you edit a tool's location, the system records a movement history entry automatically.

---

#### Tab 3 — Import (Bulk Upload)

See [Section 11 — Bulk Import Tools](#11-bulk-import-tools) for full instructions.

---

### 4.2 Dashboard — Overview & Charts

**Location:** Sidebar → Dashboard

The dashboard gives you a real-time snapshot of your tool inventory.

**Key Statistics (top cards):**

| Card | Meaning |
|---|---|
| Total Tools | Total number of tools registered |
| Usable | Tools currently in good condition |
| Scrap | Tools that have failed inspection and been retired |
| Expiring Soon | Tools whose certification expires within 30 days |
| Overdue | Tools past their expiry date |

**Charts:**

- **Tools by Site** — Bar chart showing how many tools are at each location
- **Status Distribution** — Pie chart showing usable vs. scrap split
- **Inspection Trends** — How many inspections were done over time
- **Tool Age Distribution** — Breakdown of how old tools are
- **At-Risk Tools** — Tools with low usability or nearing expiry

**Filters:** Use the dropdown at the top to filter charts by a specific user or site.

**Export:** Click the **Export** button to download a data snapshot.

---

### 4.3 Reports

**Location:** Sidebar → Reports

Use this page to search, filter, and export tool data.

- Type in the **search box** to find tools by any field (description, QR code, site, subcontractor, etc.).
- Use **column filters** to narrow results.
- Hover over a row to see its **QR code preview**.
- Click **Download CSV** to export the visible results as a spreadsheet.

---

### 4.4 Alerts

**Location:** Sidebar → Alerts

Alerts notify you about tools that need attention.

| Alert Level | Color | Examples |
|---|---|---|
| **Critical** | Red | Tool expired, usability below 80%, tool scrapped |
| **Warning** | Yellow | Tool expiring within 30 days |
| **Info** | Blue | New tool added, new user created, inspection passed |

Click any alert to see its full details (tool ID, site, timestamp).

> **Action Required:** Critical alerts should be reviewed immediately. Expired or low-usability tools pose a safety risk.

---

### 4.5 Users Management

**Location:** Sidebar → Users

#### Add a New User

1. Click **Add User**.
2. Fill in: Full Name, Username, Email, Phone, Password, Role, Site.
3. Click **Save**.

The system will automatically create an **Info alert** notifying the admin that a new user was added.

#### Edit a User

Click the **Edit** icon next to any user to update their details, role, or assigned site.

#### Deactivate / Reactivate a User

Toggle the **Active/Inactive** switch on a user row to enable or disable their access without deleting their account.

#### Delete a User

Click the **Delete** icon. Only admins can permanently delete users.

---

## 5. Inspector Guide

**Your page:** Inspector View (you are taken here after login)

As an inspector, your job is to scan tools and record safety inspection results.

### How to Inspect a Tool

**Step 1 — Find the Tool**

- **Scan with camera:** Click the camera icon and point your device at the tool's QR sticker.
- **Upload a QR image:** Click "Upload Image" and select a photo of the QR code.
- **Search manually:** Type the tool's QR code or ID in the search box.

**Step 2 — Review Tool Details**

The system displays:
- Tool description, make, capacity, SWL
- Current site and status
- Last inspection date

**Step 3 — Fill in the Inspection Form**

| Field | Options / Notes |
|---|---|
| **Result** | Pass / Conditional / Fail |
| **Usability %** | 0–100. Slide to match your assessment |
| **Photos** | Upload photos of damage or condition |
| **Remarks** | Notes about the tool's condition |

**Step 4 — Submit**

Click **Submit Inspection**.

**What happens automatically:**
- The tool's last inspection date updates.
- The tool's usability % updates.
- If you select **Fail** → the tool is automatically marked as **Scrap**.
- If usability is **below 80%** → a **Critical Alert** is created for the admin.

> **Important:** A failed inspection permanently marks the tool as Scrap. Make sure you are certain before selecting Fail.

---

## 6. Store Manager Guide

**Your page:** Store View (you are taken here after login)

As a store manager, you manage tools entering and leaving your location.

### How to Record a Tool Transaction

**Step 1 — Scan or Search the Tool**

- Use the camera to scan the tool's QR sticker, or type the QR code manually.

**Step 2 — Choose Transaction Type**

**IN Transactions** (tool arriving at your store):

| Type | When to Use |
|---|---|
| `subcon_return` | Subcontractor returning a tool |
| `new_product` | Brand new tool arriving for the first time |
| `site_receive` | Tool transferred from another site |

**OUT Transactions** (tool leaving your store):

| Type | When to Use |
|---|---|
| `subcon_work` | Sending tool to a subcontractor for work |
| `site_transfer` | Transferring tool to another site |

**Step 3 — Fill in Details**

- **Subcontractor Name, Code, Mobile** (if applicable)
- **Target Site** (where the tool is going)
- **Remarks** (optional notes)

**Step 4 — Record Movement**

Click **Record Movement**. The system will:
- Update the tool's current site.
- Create a movement history entry with your name and timestamp.
- Display the last transaction for your confirmation.

### Incident Mode

If a tool is **damaged or missing**, switch on **Incident Mode** before recording the transaction. You will be prompted to enter a **Debit To** code to assign responsibility.

---

## 7. Worker Guide

**Your page:** Worker View (you are taken here after login)

Workers can scan any tool to view its information. No editing is allowed.

### How to Check a Tool

1. Click the **Scan** button.
2. Point your camera at the tool's QR sticker.
3. The system displays the tool's details:

| Information Shown | Details |
|---|---|
| Description & Make | What the tool is |
| Capacity & SWL | Load ratings |
| Current Site | Where the tool is supposed to be |
| Status | Usable (green) or Scrap (red) |
| Usability % | Condition rating from last inspection |
| Expiry Date | When the tool's certificate expires |
| Subcontractor Info | Who is responsible for it |

> If a tool shows as **Scrap** or has a very low usability %, do not use it. Report it to your supervisor.

---

## 8. Management Guide

**Your pages:** Dashboard, Reports, Alerts

Management users have read-only access to monitor the overall system.

- Use the **Dashboard** to review statistics and spot trends.
- Use **Reports** to search for specific tools and export data.
- Use **Alerts** to stay informed about critical safety issues.

No tools or users can be created or edited from these pages.

---

## 9. Data Entry Guide

**Your pages:** Tool Master (New Entry + Saved Tools tabs only)

Data Entry users can add and view tools at their assigned site.

Follow the same steps as the [Admin Tool Creation guide (Section 4.1)](#41-tool-master--managing-tools).

> You can only see and create tools for **your assigned site**. To access other sites, contact an admin.

---

## 10. Split Tool Matching

**Location:** Available to Workers and Admins via the Split Tool page

Some tools come in two parts (Part A + Part B) that must be used together. This feature lets you verify you have the correct matching pair before use.

### How to Match a Split Tool

**Step 1 — Scan Part A**

- Click **Scan Part A**.
- Scan or upload the QR code from the first component.
- The tool's details will appear on screen.

**Step 2 — Scan Part B**

- Click **Scan Part B**.
- Scan or upload the QR code from the second component.

**Step 3 — View the Result**

| Result | Color | Meaning |
|---|---|---|
| **Correct Combination** | Green ✅ | Parts match and both are usable — safe to use |
| **Mixed Status** | Yellow ⚠️ | Parts match but one or both are not fully usable |
| **Mismatch** | Red ❌ | Wrong combination — do NOT use together |

**Matching is based on:**
- Description must be the same
- Current site must be the same
- Make, Capacity, and SWL must match

> **Safety Rule:** Never use a mismatched combination. Always get a green result before using a two-part tool.

---

## 11. Bulk Import Tools

**Location:** Tool Master → Import tab (Admin / Data Entry)

If you need to add many tools at once, use the bulk import feature instead of entering them one by one.

### Step-by-Step

**Step 1 — Download the Template**

Click **Download Template** to get the Excel file. It contains all the required columns.

**Step 2 — Fill in the Template**

Open the file in Excel and enter one tool per row. Required columns:

| Column | Example Value |
|---|---|
| description | Clamp Head |
| make | 2022 |
| capacity | 8 Ton |
| safe_working_load | 8 Ton |
| purchaser_name | ABC Corp |
| supplier_code | SUP001 |
| date_of_supply | 2024-01-15 |
| tool_type | Erection Tools |
| metal_type | Steel |
| tool_variant | Type A |
| purchaser_contact | +1234567890 |
| job_code | JOB-001 |
| job_description | Tower Erection |
| location | Site A |

**Step 3 — Upload the File**

- Click **Upload File**.
- Select your completed Excel or PDF file.
- Click **Import**.

**Step 4 — Download Results**

When the import is complete, you can download:

- **QR Code ZIP** — A ZIP file containing a PNG QR code image for every imported tool, ready to print.
- **Excel with QR Links** — Your original file with an extra column showing each tool's QR link.

If any rows had errors (missing required fields, etc.), they will be listed so you can fix and re-import them.

---

## 12. QR Codes Explained

Every tool in the system has a **unique QR code** that acts as its digital identity.

### How QR Codes Are Generated

The system automatically creates each code from the tool's data:

```
Example: CHX892-0101
         ↑↑ ↑ ↑↑↑ ↑↑↑↑
         || | |  | Serial number
         || | |  Purchaser initials
         || | Capacity digits
         || Metal type
         |Tool variant initials
         Tool description initials
```

You don't need to create QR codes manually — the system handles it automatically.

### Printing QR Codes

1. Go to **Tool Master → Saved Tools**.
2. Find the tool and click the **QR icon**.
3. The QR code displays on screen — print it or save it as an image.
4. Stick the printed QR label on the physical tool.

### Scanning QR Codes

- **Camera scan:** Works from any role's scan screen. Point your device camera at the QR sticker.
- **Upload image:** If the camera is unavailable, photograph the sticker and upload the image.
- **Manual entry:** Type the QR code directly in the search box if scanning isn't possible.

---

## 13. Alerts Explained

The system automatically monitors tools and generates alerts when action is needed.

### When Are Alerts Created?

| Alert | Triggered When |
|---|---|
| New Tool Added | A tool is created in the system |
| New User Created | A user account is added |
| Tool Expiring Soon | Expiry date is within **30 days** |
| Tool Expired | Expiry date has passed |
| Low Usability | Inspection result is **below 80%** |
| Tool Scrapped | A tool is marked as Scrap after inspection |

### Alert Severity

- **Critical (Red):** Immediate action needed — expired tools, dangerously low usability.
- **Warning (Yellow):** Plan action soon — tools expiring within 30 days.
- **Info (Blue):** Informational only — no immediate action needed.

### Responding to Alerts

1. Go to **Alerts** in the sidebar.
2. Review all **Critical** alerts first.
3. Click an alert to see the full details (tool ID, site, timestamp).
4. Take the appropriate action (schedule inspection, replace tool, etc.).

---

## 14. Frequently Asked Questions

**Q: I can't log in. What do I do?**  
Contact your admin to verify your username and password, and that your account is set to **Active**.

---

**Q: The QR scan isn't working. What should I try?**  
- Make sure your browser has camera permission.
- Try the "Upload Image" option instead — photograph the QR sticker and upload it.
- If the code is too small or damaged, type it manually in the search box.

---

**Q: A tool is showing as Scrap but it's still usable. Can I change it?**  
Only an Admin can update a tool's status. Contact your admin to review and correct the record.

---

**Q: I made a mistake when adding a tool. Can I fix it?**  
Yes. Go to **Tool Master → Saved Tools**, find the tool, click the Edit icon, make your changes, and save.

---

**Q: The wrong QR code is on a physical tool. What do I do?**  
- Find the correct tool record in Saved Tools.
- Print the correct QR code from that record.
- Replace the sticker on the physical tool.

---

**Q: How do I know if two tool parts belong together?**  
Use the **Split Tool Matching** feature. Scan both parts — the system tells you instantly whether they are a correct combination.

---

**Q: My bulk import has errors. What do I do?**  
After import, the system lists any rows that failed. Common causes:
- Missing required fields (description, make, capacity, etc.)
- Invalid date format (use YYYY-MM-DD)
- Duplicate entries

Fix the errors in your Excel file and re-upload just those rows.

---

**Q: Can I use this on my phone?**  
Yes. The system is designed to work on mobile browsers. The QR scanning features use your phone's camera. Use Chrome or Safari for best results.

---

**Q: How long are tool records kept?**  
Tool records, inspection history, and movement logs are kept indefinitely in the system. Admins can export historical data as a PDF report covering the last 12 months.

---

*For technical support or to report an issue, contact your system administrator.*
