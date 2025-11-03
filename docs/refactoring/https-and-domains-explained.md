# HTTPS and Domains - Explained Simply

This guide explains how HTTPS, SSL certificates, nginx-proxy, and domains work using simple analogies. Perfect for understanding the complete deployment setup!

## Table of Contents
1. [Understanding Domains](#understanding-domains)
2. [The HTTPS Setup Explained](#the-https-setup-explained)
3. [How Everything Works Together](#how-everything-works-together)
4. [Practical Setup Guide](#practical-setup-guide)

---

# Part 1: Understanding Domains

## What is a Domain?

Imagine the internet is like a giant city with billions of houses (computers/servers).

### Without Domains (Just IP Addresses):

```
You: "I want to visit Google!"
Computer: "Okay, go to 142.250.80.46"
You: "Wait... what??"

You: "I want to watch YouTube!"
Computer: "Go to 172.217.164.206"
You: "How am I supposed to remember that??"

You: "I want to check Facebook!"
Computer: "Go to 157.240.241.35"
You: "This is impossible!"
```

**IP Address = House address with just numbers**
- Like saying "I live at house number 192.168.1.100"
- Hard to remember!
- Not meaningful

### With Domains (Friendly Names):

```
You: "I want to visit Google!"
Computer: "Okay, go to google.com"
You: "Easy to remember!"

You: "I want to watch YouTube!"
Computer: "Go to youtube.com"
You: "I can remember that!"

You: "I want to check Facebook!"
Computer: "Go to facebook.com"
You: "Perfect!"
```

**Domain = Friendly name for a house**
- Like saying "I live at Bob's House"
- Easy to remember!
- Meaningful and descriptive

---

## How Domains Work - The Complete Journey

```
Step 1: You type in your browser
┌─────────────────────┐
│  www.google.com     │
└─────────────────────┘

Step 2: Your computer asks "What's the address?"
Your Computer: "I need to find google.com"
Your Computer: "Let me check my phone book..."

Step 3: DNS Lookup (The Internet's Phone Book)
┌──────────────────────────────────────┐
│         DNS Server                   │
│    (Like a giant phone book)         │
│                                      │
│  google.com ────────▶ 142.250.80.46 │
│  youtube.com ───────▶ 172.217.164.206│
│  facebook.com ──────▶ 157.240.241.35 │
│  survey.example.com ▶ 123.45.67.89  │
└──────────────────────────────────────┘

Step 4: DNS Server responds
DNS Server: "google.com is at 142.250.80.46"

Step 5: Your computer connects
Your Computer: *connects to 142.250.80.46*

Step 6: You see Google!
Browser: Shows Google homepage
```

---

## Domain Structure

```
Full Domain: www.survey.example.com

Breaking it apart:
┌──────────────────────────────────────────┐
│  www  .  survey  .  example  .  com      │
│  └┬┘     └──┬──┘    └───┬──┘    └┬┘     │
│   │         │            │        │      │
│  Sub-    Subdomain    Domain    TLD     │
│ domain                 Name              │
└──────────────────────────────────────────┘
```

### 1. TLD (Top-Level Domain) = Country

```
.com  = Commercial/Business
.org  = Organization
.edu  = Education
.gov  = Government
.uk   = United Kingdom
.de   = Germany
```

### 2. Domain Name = City/Street

**This is what YOU buy/register!**

How to get one:
1. Go to a domain registrar (GoDaddy, Namecheap, Google Domains, Cloudflare)
2. Search if the name is available
3. Pay yearly fee (usually $10-20/year)
4. Now you own that domain!

### 3. Subdomain = Apartment/Room Number

```
www.survey.example.com
└┬┘
 Subdomain (you can create these for FREE)

Other examples:
api.survey.example.com
blog.survey.example.com
shop.survey.example.com
```

**Analogy:**
```
You own: "Bob's Building"
You can create free apartments:
- "Apartment A, Bob's Building"  → www.example.com
- "Apartment B, Bob's Building"  → api.example.com
- "Penthouse, Bob's Building"    → blog.example.com
```

---

## Domain vs IP Address - Summary

```
IP Address (123.45.67.89):
❌ Hard to remember
❌ Looks scary/untrustworthy
❌ Changes if you switch servers
❌ Can't get SSL certificate
❌ Not professional

Domain (hmc-survey.com):
✅ Easy to remember
✅ Professional and trustworthy
✅ Can change servers, keep same domain
✅ Can get SSL certificate (HTTPS)
✅ Can create subdomains for free
✅ Better for SEO
```

---

# Part 2: The HTTPS Setup Explained

## The Big Picture: Your Website's Journey

Think of your dashboard as a **lemonade stand**, and you want people from all over town to buy lemonade safely.

### Basic Setup (HTTP Only)

```
┌─────────────────────────────────────────────────────┐
│              Your House (Server)                    │
│                                                     │
│  ┌──────────┐         ┌──────────────┐            │
│  │ Friend   │────────▶│  Lemonade    │            │
│  │ (nginx)  │         │  Stand       │            │
│  │          │         │ (dashboard)  │            │
│  └──────────┘         └──────────────┘            │
│       │                                            │
│  ┌────▼─────────────────────────────────┐         │
│  │  Door to street (Port 80)            │         │
│  │  Anyone can walk in                  │         │
│  └──────────────────────────────────────┘         │
└─────────────────────────────────────────────────────┘
         │
    ┌────▼────┐
    │ People  │
    │ on the  │
    │ street  │
    └─────────┘
```

**The problem:** Bad guys can see what people are saying! They can read passwords and steal information.

---

## Why We Need HTTPS (The Lock on Your Door)

```
WITHOUT HTTPS (HTTP):
Person: "My password is SECRET123"
Bad Guy: *listening* "Haha, I heard that!"

WITH HTTPS:
Person: "Kj#8$mF@2%qZ" (encrypted, looks like gibberish)
Bad Guy: *listening* "What?? I can't understand anything!"
```

**HTTPS = HTTP + Secure**
- It's like putting messages in a **locked box** that only you and the visitor can open
- Even if bad guys intercept the box, they can't open it

---

## The Complete HTTPS Setup

```
┌──────────────────────────────────────────────────────────┐
│                   Your House (Server)                    │
│                                                          │
│  ┌────────────┐  "Need SSL    ┌──────────────┐         │
│  │  Security  │   for Bob's   │   Friendly   │         │
│  │  Guard     │   house!"     │   Security   │         │
│  │ (acme-     │◀─────────────▶│   Company    │         │
│  │ companion) │  "Here's a    │ (Let's       │         │
│  │            │   certificate"│  Encrypt)    │         │
│  └─────┬──────┘               └──────────────┘         │
│        │                                                │
│        │ "I got the certificate!"                       │
│        ▼                                                │
│  ┌──────────────┐       ┌──────────────┐              │
│  │ Smart Friend │──────▶│  Lemonade    │              │
│  │ (nginx-proxy)│       │  Stand       │              │
│  │              │       │ (dashboard)  │              │
│  │ *Has lock*   │       │              │              │
│  └──────┬───────┘       └──────────────┘              │
│         │                                              │
│  ┌──────▼──────────────────────────────────┐          │
│  │  🔒 Locked Door (Port 443 - HTTPS)      │          │
│  │  🚪 Regular Door (Port 80 - HTTP)       │          │
│  └─────────────────────────────────────────┘          │
└──────────────────────────────────────────────────────────┘
              │
         ┌────▼────┐
         │ People  │
         │ with    │
         │ secrets │
         └─────────┘
```

---

## Meet the Team Members

### 1. Dashboard (Your Lemonade Stand)

**What it is:** Your actual app - the survey dashboard

**What it does:**
- Shows charts and graphs
- Lets people click buttons and filters
- Serves data visualizations

**Analogy:**
> "This is your lemonade stand. It makes the lemonade (data visualizations) and serves customers."

---

### 2. nginx-proxy (The Smart Friend)

**What it is:** A special helper that stands at your door

**What it does:**
- Greets everyone who comes to your house
- Asks "Who are you looking for?"
- Sends them to the right room
- Locks all messages in secure boxes (HTTPS)

**The magic part:**
- It's **smart** - it watches what's happening in your house
- When you add a new lemonade stand, it automatically knows!
- You don't have to tell it manually

**How it watches:**
```
You: *starts a new lemonade stand*
You: *puts a sign: "My address is lemonade.com"*

Smart Friend: *sees the sign through a special window*
Smart Friend: "Oh! New stand! I'll tell visitors how to get there!"
```

**That special window = Docker Socket**

**Analogy:**
> "The smart friend sits at your door and directs visitors. If you hang a sign saying 'Lemonade Stand at 123 Main Street', the friend automatically learns it and tells visitors where to go!"

---

### 3. acme-companion (The Security Guard)

**What it is:** A security guard who gets you special security certificates

**What it does:**
- Goes to a security company (Let's Encrypt)
- Says "My friend needs a lock for their door"
- Proves you own the house
- Gets the lock
- Installs it on your door

**The proving part (ACME Challenge):**
```
Security Company: "Put this special flag outside your house"
Security Guard: *puts flag outside*
Security Company: *drives by, sees flag*
Security Company: "Yep, you own that house! Here's your lock!"
```

**The renewal part:**
- Locks expire after 90 days (for safety)
- Security guard automatically gets new locks before they expire
- You never have to think about it!

**Analogy:**
> "The security guard is like a responsible adult who makes sure all your doors have working locks. Every few months, they get new locks from the lock store (Let's Encrypt)."

---

### 4. Docker Socket (The Special Window)

**What it is:** A magic window that lets containers see what's happening

**Analogy:**
```
Regular Setup:
┌─────────────────────┐
│  Room 1             │  Can't see other rooms
└─────────────────────┘

┌─────────────────────┐
│  Room 2             │  Can't see other rooms
└─────────────────────┘

With Docker Socket:
┌─────────────────────┐
│  Room 1             │
│  ┌──────────┐       │
│  │ Window ──┼───────┼──▶ Can see when new rooms are built!
│  └──────────┘       │     Can see signs in rooms!
└─────────────────────┘
```

**What it does:**
- Lets nginx-proxy watch for new containers
- Lets nginx-proxy see their signs (VIRTUAL_HOST environment variables)
- Lets acme-companion watch for security requests

**Why it's safe:**
- We give them a **read-only** window (`:ro`)
- They can look, but can't touch
- Like a one-way mirror

**Analogy:**
> "Your house has a special window where your smart friend can see all the room signs but can't enter or mess with the rooms. They just watch and help direct traffic."

---

## The Environment Variables (The Signs You Hang)

Think of environment variables as **signs you hang on your door**.

### VIRTUAL_HOST=survey.example.com

```
┌─────────────────────────┐
│  Lemonade Stand         │
│                         │
│  📋 Sign on door:       │
│  "Address:              │
│   survey.example.com"   │
└─────────────────────────┘
         │
         ▼
nginx-proxy sees this sign:
"When someone asks for survey.example.com,
 I should send them to THIS container!"
```

**Analogy:**
> "It's like putting your house number on your mailbox so the mailman knows where to deliver letters."

---

### VIRTUAL_PROTO=http

```
┌─────────────────────────┐
│  Lemonade Stand         │
│                         │
│  📋 Sign on door:       │
│  "I speak regular       │
│   language (HTTP),      │
│   not secret language"  │
└─────────────────────────┘
```

**Why this matters:**
- Outside world ↔ nginx-proxy: HTTPS (encrypted, secure)
- nginx-proxy ↔ dashboard: HTTP (regular, no encryption needed)

**Why no encryption inside?**
- They're in the same house (Docker network)
- Like talking to your sister in your bedroom - no one else can hear
- Encryption would be unnecessary!

**Analogy:**
> "When you talk to your mom inside the house, you speak normally. But when you shout to your friend across the street, you use a secret code. This sign says 'I'm inside the house, speak normally!'"

---

### LETSENCRYPT_HOST=survey.example.com

```
┌─────────────────────────┐
│  Lemonade Stand         │
│                         │
│  📋 Sign on door:       │
│  "Security guard,       │
│   please get me a lock  │
│   for survey.example.com"│
└─────────────────────────┘
         │
         ▼
acme-companion sees this:
"Going to Let's Encrypt to get
 an SSL certificate!"
```

**Analogy:**
> "This is like asking your parent to get you a lock from the hardware store. The sign tells them which lock you need."

---

### LETSENCRYPT_EMAIL=you@example.com

```
┌─────────────────────────┐
│  Lemonade Stand         │
│                         │
│  📋 Sign on door:       │
│  "If my lock breaks,    │
│   email: you@example.com"│
└─────────────────────────┘
```

**What Let's Encrypt does with this:**
- Sends emails when certificate is about to expire
- Sends security notifications
- Like giving the lock store your phone number

---

## The Folders (Where Things Are Stored)

### ./nginx/certs/ (The Lock Cabinet)

```
┌─────────────────────────────┐
│  Lock Cabinet               │
│                             │
│  📁 survey.example.com.crt  │  (The actual lock)
│  🔑 survey.example.com.key  │  (The key to the lock)
│                             │
│  These are your SSL certs   │
└─────────────────────────────┘
```

**Who uses it:**
- acme-companion: Writes new locks here
- nginx-proxy: Reads locks to secure connections

**Analogy:**
> "This is like a drawer where you keep all your padlocks and keys."

---

### ./nginx/html/ (The Proof Box)

```
┌─────────────────────────────┐
│  Proof Box                  │
│                             │
│  📄 .well-known/            │
│      acme-challenge/        │
│        RANDOM_TOKEN         │
│                             │
│  Temporary files to prove   │
│  you own the domain         │
└─────────────────────────────┘
```

**How it's used (ACME Challenge):**
```
Let's Encrypt: "Put this secret code in a file on your website"
acme-companion: *creates file*
Let's Encrypt: *visits http://survey.example.com/.well-known/acme-challenge/SECRET*
Let's Encrypt: "Found it! You own this domain. Here's your certificate!"
```

**Analogy:**
> "The lock store says 'Prove this is your house by putting a red flag in your mailbox.' You put the flag, they drive by and see it, then give you the lock."

---

### ./nginx/vhost.d/ (Custom Room Decorations)

```
┌─────────────────────────────┐
│  Custom Decorations         │
│                             │
│  📄 survey.example.com      │
│     (special nginx config   │
│      just for this domain)  │
└─────────────────────────────┘
```

**What you can put here:**
- Custom nginx settings for specific domains
- WebSocket configuration
- Rate limiting
- Custom headers

**Analogy:**
> "nginx-proxy automatically decorates your rooms, but if you want special wallpaper in one room, you put it here and nginx-proxy will add it."

---

### acme-data volume (The Security Guard's Notebook)

```
┌─────────────────────────────┐
│  Security Guard's Notebook  │
│                             │
│  📓 Account with Let's      │
│     Encrypt                 │
│  📓 History of certificates │
│  📓 Private account key     │
│                             │
│  Managed by Docker          │
└─────────────────────────────┘
```

**Why it's a "named volume":**
- Docker manages it in a special place
- Survives even if you delete containers
- Like a safety deposit box

---

# Part 3: How Everything Works Together

## Scenario: Someone Visits Your Website

```
Step 1: Alice types in her browser
┌────────────────────────────┐
│ https://survey.example.com │
└────────────────────────────┘

Step 2: DNS Lookup
"Where is survey.example.com?"
"It's at 123.45.67.89!"

Step 3: Request travels to your server
Internet ─────────▶ Your Server (Port 443)

Step 4: nginx-proxy answers
nginx-proxy: "Hello! Who are you looking for?"
Request: "I want survey.example.com"
nginx-proxy: "Let me lock your messages first..." 🔒
nginx-proxy: "That's the dashboard. I'll take you there!"

Step 5: nginx-proxy forwards to dashboard
nginx-proxy ──────▶ dashboard container

Step 6: Dashboard responds
dashboard: "Here are your charts!"

Step 7: nginx-proxy sends response back
nginx-proxy: *locks the response* 🔒
nginx-proxy ──────▶ Alice

Step 8: Alice sees the dashboard
Alice: "Yay! Pretty charts! And it's secure!" 🎉
```

---

## Scenario: Adding a New Service

```
Step 1: You create a new container
docker run ... -e VIRTUAL_HOST=de.survey.example.com

Step 2: nginx-proxy watches
nginx-proxy: "Oh! New room with a sign!"
nginx-proxy: *automatically creates route*

Step 3: acme-companion watches
acme-companion: "New LETSENCRYPT_HOST!"
acme-companion: "Getting SSL certificate..."

Step 4: Certificate request
acme-companion ──▶ Let's Encrypt
Let's Encrypt ──▶ *verifies domain*
Let's Encrypt ──▶ "Here's your certificate"

Step 5: Everything updates automatically
Done! https://de.survey.example.com is live! 🎉
```

---

## How It Starts Up

```
⏰ Time: 0s - Docker Compose reads config
⏰ Time: 1s - Creates network
⏰ Time: 2s - Starts nginx-proxy
⏰ Time: 5s - Starts acme-companion
⏰ Time: 7s - Starts dashboard (hangs VIRTUAL_HOST sign)
⏰ Time: 8s - nginx-proxy sees sign, creates route
⏰ Time: 9s - acme-companion sees sign, requests certificate
⏰ Time: 10-180s - Let's Encrypt verifies and issues certificate
⏰ Time: 180s+ - HTTPS is live! ✅
```

---

# Part 4: Practical Setup Guide

## Step 1: Get a Domain

1. Go to a domain registrar:
   - Namecheap.com
   - Google Domains
   - Cloudflare.com

2. Search for available domain:
   ```
   hmc-survey.com
   survey-explorer.com
   hmc-data.org
   ```

3. Buy it ($10-20/year)

4. Point it to your server:
   ```
   DNS Settings:
   Type: A Record
   Host: @
   Value: YOUR_SERVER_IP
   TTL: Automatic
   ```

5. Wait for DNS propagation (5 minutes to 1 hour)

---

## Step 2: Update Your Configuration

In `.env`:
```bash
# Production domain
HOST=survey.example.com

# Email for Let's Encrypt
LETSENCRYPT_EMAIL=your-email@example.com
```

---

## Step 3: Start the Containers

```bash
docker-compose up -d
```

Watch the magic happen:
```bash
docker-compose logs -f
```

You'll see:
- nginx-proxy starts
- acme-companion starts
- Dashboard starts and hangs VIRTUAL_HOST sign
- acme-companion requests SSL certificate
- Let's Encrypt verifies domain
- Certificate issued
- HTTPS enabled!

---

## Step 4: Visit Your Site

Go to: `https://survey.example.com`

You should see:
- 🔒 Lock icon in browser
- Your dashboard loads
- Everything is secure!

---

## Troubleshooting

### Domain doesn't resolve
```
Problem: Can't reach your domain
Check: dig survey.example.com
Should show: Your server IP
Fix: Wait for DNS propagation or check DNS settings
```

### Let's Encrypt can't verify domain
```
Problem: Certificate request fails
Check: Port 80 must be open
Check: Domain must point to your server
Check: ./nginx/html/ must be accessible
```

### Certificate not auto-renewing
```
Problem: Certificate expires
Check: acme-companion container is running
Check: Logs: docker-compose logs acme-companion
Fix: Restart acme-companion
```

---

## Summary

```
The Complete Picture:

1. You buy a domain (survey.example.com)
2. Point domain to your server IP
3. Set VIRTUAL_HOST=survey.example.com on your container
4. Set LETSENCRYPT_HOST=survey.example.com
5. nginx-proxy auto-creates route
6. acme-companion auto-gets SSL certificate
7. HTTPS automatically enabled
8. Certificate auto-renews every 60 days

Result: Professional, secure website with minimal effort!
```

---

## Key Takeaways

**Domains:**
- Friendly names for IP addresses
- Like putting "Bob's House" instead of "House #12345678"
- Required for HTTPS (Let's Encrypt needs domains)
- Cost: ~$12/year

**HTTPS:**
- Encrypts data between user and server
- Like putting messages in locked boxes
- Required for security and trust
- Free with Let's Encrypt

**Automation:**
- nginx-proxy watches for new containers
- Automatically creates routes
- acme-companion automatically gets SSL
- You just set environment variables

**Magic Ingredients:**
- Docker Socket: The special window for watching
- Environment Variables: The signs you hang
- Let's Encrypt: The free lock store
- nginx-proxy: The smart friend at your door
- acme-companion: The security guard

---

## Next Steps

Now that you understand how everything works:

1. Register your domain
2. Update docker-compose.yml (we'll do this together)
3. Deploy to production
4. Watch HTTPS magically appear!

The beauty of this setup is that once it's configured, everything is automatic. Add a new service? Just set the environment variables and it works!
