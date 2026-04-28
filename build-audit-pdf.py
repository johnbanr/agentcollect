#!/usr/bin/env python3
"""
Build IWS AR Collection Audit PDF - Light, clean, McKinsey-style
Professional audit report. Fond clair. Pas un pitch.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
import os

# Colors - Light theme
BG = white
TEXT = HexColor('#0B1B3D')
TEXT_SECONDARY = HexColor('#374151')
MUTED = HexColor('#6B7280')
LIGHT_MUTED = HexColor('#9CA3AF')
BORDER = HexColor('#E5E7EB')
LIGHT_BG = HexColor('#F9FAFB')
CARD_BG = HexColor('#F3F4F6')
RED = HexColor('#DC2626')
RED_LIGHT = HexColor('#FEF2F2')
RED_BORDER = HexColor('#FECACA')
AMBER = HexColor('#D97706')
AMBER_LIGHT = HexColor('#FFFBEB')
AMBER_BORDER = HexColor('#FDE68A')
GREEN = HexColor('#059669')
BLUE = HexColor('#4F46E5')
BLUE_LIGHT = HexColor('#EEF2FF')
DARK_BG = HexColor('#0B1B3D')

W, H = letter
OUT = '/Users/jonathanbanner/github/agentcollect/audit-iws-report.pdf'
M = 60  # margin

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle("AR Collection Audit: Interstate Waste Services")
c.setAuthor("AgentCollect")
c.setSubject("Confidential AR Audit - April 2026")


def page_header(c, page_num):
    """Standard page header for pages 2-7"""
    # Top line accent
    c.setFillColor(BLUE)
    c.rect(0, H - 3, W, 3, fill=1, stroke=0)
    # Header text
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8)
    c.drawString(M, H - 28, "INTERSTATE WASTE SERVICES")
    c.setFillColor(BORDER)
    c.drawString(M + 155, H - 28, "|")
    c.setFillColor(MUTED)
    c.drawString(M + 163, H - 28, "AR COLLECTION AUDIT")
    c.drawRightString(W - M, H - 28, f"PAGE {page_num} OF 7")
    # Divider
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(M, H - 38, W - M, H - 38)


def page_footer(c):
    """Standard footer"""
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(M, 45, W - M, 45)
    c.setFillColor(LIGHT_MUTED)
    c.setFont('Helvetica', 7)
    c.drawString(M, 32, "CONFIDENTIAL")
    c.drawRightString(W - M, 32, "AgentCollect (YC S23)")


def draw_rounded_rect(c, x, y, w, h, r, fill_color, stroke_color=None, stroke_width=0.5):
    c.saveState()
    c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
        c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    c.restoreState()


def severity_badge(c, x, y, text, color, bg_color, border_color):
    tw = c.stringWidth(text, 'Helvetica-Bold', 7) + 14
    draw_rounded_rect(c, x, y - 3, tw, 15, 3, bg_color, border_color, 0.5)
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(x + 7, y + 1, text)
    return tw


def score_bar(c, x, y, w, score, max_score=10, color=RED):
    draw_rounded_rect(c, x, y, w, 6, 2, CARD_BG)
    fill_w = (score / max_score) * w
    if fill_w > 3:
        draw_rounded_rect(c, x, y, fill_w, 6, 2, color)


# ================================================
# PAGE 1: COVER
# ================================================
# White background
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Top accent bar
c.setFillColor(BLUE)
c.rect(0, H - 4, W, 4, fill=1, stroke=0)

# Left accent stripe
c.setFillColor(BLUE)
c.rect(M - 8, H / 2 - 60, 4, 180, fill=1, stroke=0)

# AgentCollect logo
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 13)
c.drawString(M, H - 50, "AgentCollect")
c.setFillColor(BLUE)
c.circle(M + c.stringWidth("AgentCollect", 'Helvetica-Bold', 13) + 4, H - 44, 2.5, fill=1, stroke=0)

# Confidential
c.setFillColor(MUTED)
c.setFont('Helvetica', 9)
c.drawRightString(W - M, H - 50, "CONFIDENTIAL")

# Main title
y_title = H / 2 + 100
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 44)
c.drawString(M, y_title, "Interstate")
c.drawString(M, y_title - 52, "Waste Services")

# Subtitle
c.setFillColor(MUTED)
c.setFont('Helvetica', 20)
c.drawString(M, y_title - 100, "AR Collection Audit")

# Date & details
c.setFont('Helvetica', 13)
c.drawString(M, y_title - 130, "April 2026")

# Bottom details
y_bot = 100
c.setStrokeColor(BORDER)
c.setLineWidth(0.5)
c.line(M, y_bot + 30, W - M, y_bot + 30)

c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 10)
c.drawString(M, y_bot + 10, "Prepared by AgentCollect (YC S23)")
c.setFillColor(MUTED)
c.setFont('Helvetica', 9)
c.drawString(M, y_bot - 8, "8 recorded calls  |  3 caller personas  |  4 portal tests")

c.setFillColor(MUTED)
c.setFont('Helvetica', 9)
c.drawRightString(W - M, y_bot + 10, "j@agentcollect.com")
c.drawRightString(W - M, y_bot - 8, "(415) 867-4010")

c.showPage()


# ================================================
# PAGE 2: EXECUTIVE SUMMARY
# ================================================
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)
page_header(c, 2)

# Title
y = H - 70
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 24)
c.drawString(M, y, "Executive Summary")

# Overall score card
y_sc = y - 50
draw_rounded_rect(c, M, y_sc - 65, W - 2 * M, 70, 8, LIGHT_BG, BORDER)

# Score
c.setFillColor(RED)
c.setFont('Helvetica-Bold', 48)
c.drawString(M + 20, y_sc - 50, "2.1")
c.setFillColor(MUTED)
c.setFont('Helvetica', 18)
c.drawString(M + 95, y_sc - 42, "/10")

c.setFillColor(MUTED)
c.setFont('Helvetica', 9)
c.drawString(M + 20, y_sc - 5, "OVERALL SCORE")

# Metrics
mx = 200
c.setFillColor(RED)
c.setFont('Helvetica-Bold', 22)
c.drawString(mx, y_sc - 30, "$48,124")
c.setFillColor(MUTED)
c.setFont('Helvetica', 9)
c.drawString(mx, y_sc - 48, "disclosed to strangers")

c.setFillColor(RED)
c.setFont('Helvetica-Bold', 22)
c.drawString(mx + 130, y_sc - 30, "$0")
c.setFillColor(MUTED)
c.setFont('Helvetica', 9)
c.drawString(mx + 130, y_sc - 48, "collected")

c.setFillColor(RED)
c.setFont('Helvetica-Bold', 22)
c.drawString(mx + 210, y_sc - 30, "$4.8M+")
c.setFillColor(MUTED)
c.setFont('Helvetica', 9)
c.drawString(mx + 210, y_sc - 48, "at risk annually")

# Category scores
y_cat = y_sc - 100
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 13)
c.drawString(M, y_cat, "Category Scores")

categories = [
    ("Identity Verification", 0, RED, "CRITICAL"),
    ("Empathy & Helpfulness", 3, AMBER, "LOW"),
    ("Dispute Resolution", 0, RED, "CRITICAL"),
    ("Payment Collection", 0, RED, "CRITICAL"),
    ("After-Hours Coverage", 0, RED, "CRITICAL"),
    ("Online Portal", 0, RED, "BROKEN"),
]

y_row = y_cat - 28
for label, score, color, sev in categories:
    draw_rounded_rect(c, M, y_row - 3, W - 2 * M, 25, 4, BG, BORDER)

    c.setFillColor(TEXT_SECONDARY)
    c.setFont('Helvetica', 10)
    c.drawString(M + 12, y_row + 3, label)

    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(260, y_row + 2, f"{score}/10")

    score_bar(c, 310, y_row + 4, 100, score, 10, color)

    bg_c = RED_LIGHT if color == RED else AMBER_LIGHT
    bd_c = RED_BORDER if color == RED else AMBER_BORDER
    severity_badge(c, 425, y_row + 3, sev, color, bg_c, bd_c)

    y_row -= 32

# Methodology
y_meth = y_row - 20
draw_rounded_rect(c, M, y_meth, W - 2 * M, 45, 6, LIGHT_BG, BORDER)
c.setFillColor(MUTED)
c.setFont('Helvetica-Bold', 8)
c.drawString(M + 14, y_meth + 28, "METHODOLOGY")
c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 9)
c.drawString(M + 14, y_meth + 13, "8 calls  |  3 caller personas  |  4 portal URL tests  |  1 IVR analysis")
c.drawString(M + 14, y_meth + 1, "April 4, 2026  |  (866) 342-5497  |  All calls recorded")

# Key bottom stat
y_ks = y_meth - 45
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 13)
c.drawCentredString(W / 2, y_ks, "Your team disclosed $48,124 and collected $0.")

page_footer(c)
c.showPage()


# ================================================
# PAGE 3: FINDING #1 - NO IDENTITY VERIFICATION
# ================================================
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)
page_header(c, 3)

y = H - 65
# Finding badge
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 10)
c.drawString(M, y, "FINDING 1")
severity_badge(c, M + 70, y, "CRITICAL", RED, RED_LIGHT, RED_BORDER)

c.setFillColor(RED)
c.setFont('Helvetica-Bold', 10)
c.drawRightString(W - M, y, "0 / 10")

# Title
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 22)
c.drawString(M, y - 30, "No Identity Verification")

# Subtitle
c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 12)
c.drawString(M, y - 52, "$34,818 in account data disclosed to an unverified caller")
c.drawString(M, y - 68, "in a single 15-minute phone call.")

# Divider
c.setStrokeColor(BORDER)
c.line(M, y - 82, W - M, y - 82)

# Transcript card
y_t = y - 100
draw_rounded_rect(c, M, y_t - 175, W - 2 * M, 180, 8, LIGHT_BG, BORDER)

c.setFillColor(MUTED)
c.setFont('Helvetica-Bold', 8)
c.drawString(M + 14, y_t - 8, "TRANSCRIPT EXCERPT")
c.setFillColor(LIGHT_MUTED)
c.setFont('Helvetica', 8)
c.drawString(M + 130, y_t - 8, "CityMD Vendor Reconciliation  |  Duration: 15:25")

lines = [
    ("CALLER (STACEY)", "agent", '"Hi, this is Stacey James over at CityMD in Jersey City.'),
    ("", "agent", "I'm doing our monthly vendor check.\""),
    ("", "", ""),
    ("CHARLENE (IWS)", "rep", '"I\'ll be happy to assist you with that, Stacy.'),
    ("", "rep", 'Can you provide me with the account address?"'),
    ("", "note", "[No account number asked. No callback verification.]"),
    ("", "", ""),
    ("CHARLENE (IWS)", "rep", '"Your balance is $34,818.38."'),
    ("", "note", "[+ payment history, AP email ap@citymd.net, contact Lizbeth Rutherford]"),
]

y_line = y_t - 28
for speaker, role, text in lines:
    if speaker:
        color_s = BLUE if role == "agent" else TEXT
        c.setFillColor(color_s)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(M + 14, y_line, speaker)
        y_line -= 12
    if text:
        if role == "note":
            c.setFillColor(RED)
            c.setFont('Helvetica-Oblique', 8)
        else:
            c.setFillColor(TEXT_SECONDARY)
            c.setFont('Courier', 9)
        c.drawString(M + 14, y_line, text)
        y_line -= 14
    else:
        y_line -= 6

# Data disclosed
y_data = y_t - 200
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 12)
c.drawString(M, y_data, "Data Disclosed Without Verification")

items = [
    "Full account balance ($34,818.38)",
    "AP email (ap@citymd.net)",
    "Primary contact (Lizbeth Rutherford)",
    "Payment history (3 open invoices)",
    "Service details (cardboard 2x/wk, trash 6x/wk)",
    "Customer address (340 Grove St, Jersey City NJ)",
]

y_item = y_data - 22
for item in items:
    # Red check
    c.setFillColor(RED)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(M + 8, y_item, "+")
    c.setFillColor(TEXT_SECONDARY)
    c.setFont('Helvetica', 10)
    c.drawString(M + 24, y_item, item)
    y_item -= 18

# Not needed
c.setFillColor(LIGHT_MUTED)
c.setFont('Helvetica', 10)
c.drawString(M + 8, y_item, "-")
c.drawString(M + 24, y_item, "Account number -- not asked, not needed")

# Audio link
y_audio = y_item - 35
draw_rounded_rect(c, M, y_audio - 2, W - 2 * M, 24, 5, BLUE_LIGHT, HexColor('#C7D2FE'))
c.setFillColor(BLUE)
c.setFont('Helvetica-Bold', 9)
c.drawString(M + 12, y_audio + 4, "HEAR THE FULL RECORDING:")
c.setFillColor(HexColor('#4338CA'))
c.setFont('Helvetica', 9)
c.drawString(M + 190, y_audio + 4, "agentcollect.com/audit-iws")

page_footer(c)
c.showPage()


# ================================================
# PAGE 4: FINDING #2 - PATTERN + FINDING #3 - DISPUTES
# ================================================
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)
page_header(c, 4)

y = H - 65
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 10)
c.drawString(M, y, "FINDING 2")
severity_badge(c, M + 70, y, "PATTERN", AMBER, AMBER_LIGHT, AMBER_BORDER)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 22)
c.drawString(M, y - 30, "Confirmed: Systemic")

c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 12)
c.drawString(M, y - 52, "Second call, different rep, same zero verification.")
c.drawString(M, y - 68, "$13,305 disclosed with full equipment inventory.")

c.setStrokeColor(BORDER)
c.line(M, y - 82, W - M, y - 82)

# Transcript card
y_t = y - 100
draw_rounded_rect(c, M, y_t - 120, W - 2 * M, 125, 8, LIGHT_BG, BORDER)

c.setFillColor(MUTED)
c.setFont('Helvetica-Bold', 8)
c.drawString(M + 14, y_t - 8, "TRANSCRIPT EXCERPT")
c.setFillColor(LIGHT_MUTED)
c.setFont('Helvetica', 8)
c.drawString(M + 130, y_t - 8, "Chelsea Piers Vendor Call  |  Duration: 12:00")

lines2 = [
    ("CALLER (SARAH)", "agent", '"Hi, this is Sarah Piacentini from Chelsea Piers."'),
    ("", "", ""),
    ("SUE (IWS)", "rep", '"Okay, let me look you up."'),
    ("", "note", "[No account number. No callback. No verification.]"),
    ("", "", ""),
    ("SUE (IWS)", "rep", '"Your balance is $13,305.68. Last charge was March 16."'),
    ("", "note", "[+ 2x 30-yard dumpsters, 12x recycling bins, 5x trash, daily pickup, contacts]"),
]

y_line = y_t - 28
for speaker, role, text in lines2:
    if speaker:
        color_s = BLUE if role == "agent" else TEXT
        c.setFillColor(color_s)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(M + 14, y_line, speaker)
        y_line -= 12
    if text:
        if role == "note":
            c.setFillColor(RED)
            c.setFont('Helvetica-Oblique', 8)
        else:
            c.setFillColor(TEXT_SECONDARY)
            c.setFont('Courier', 9)
        c.drawString(M + 14, y_line, text)
        y_line -= 14
    else:
        y_line -= 6

# Combined exposure
y_comb = y_t - 150
draw_rounded_rect(c, M, y_comb, W - 2 * M, 40, 6, RED_LIGHT, RED_BORDER)
c.setFillColor(RED)
c.setFont('Helvetica-Bold', 14)
c.drawCentredString(W / 2, y_comb + 20, "Combined Exposure: $48,124 in 2 Calls")
c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 9)
c.drawCentredString(W / 2, y_comb + 5, "Two reps. Two callers. Same zero-verification process.")

# FINDING 3
y_f3 = y_comb - 40
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 10)
c.drawString(M, y_f3, "FINDING 3")
severity_badge(c, M + 70, y_f3, "CRITICAL", RED, RED_LIGHT, RED_BORDER)
c.setFillColor(RED)
c.setFont('Helvetica-Bold', 10)
c.drawRightString(W - M, y_f3, "0 / 10")

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 18)
c.drawString(M, y_f3 - 28, "Disputes Go Nowhere")

c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 11)
c.drawString(M, y_f3 - 50, "A customer calls about a missed dumpster pickup at Glen Pointe.")
c.drawString(M, y_f3 - 65, "Nancy confirms the account (no verification). The customer asks for a credit.")

# Quote box
y_q = y_f3 - 95
draw_rounded_rect(c, M + 20, y_q, W - 2 * M - 40, 35, 6, LIGHT_BG, BORDER)

# Left accent bar on quote
c.setFillColor(RED)
c.rect(M + 20, y_q, 3, 35, fill=1, stroke=0)

c.setFillColor(TEXT)
c.setFont('Courier', 10)
c.drawString(M + 34, y_q + 18, '"You\'ll need to speak with your sales rep,')
c.drawString(M + 34, y_q + 4, ' David, about that."')
c.setFillColor(MUTED)
c.setFont('Helvetica-Oblique', 9)
c.drawRightString(W - M - 30, y_q + 4, "Nancy, IWS Billing")

c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 10)
c.drawString(M, y_q - 22, "The customer called billing. Billing can't resolve it.")
c.drawString(M, y_q - 36, "That customer is now looking at competitors.")

page_footer(c)
c.showPage()


# ================================================
# PAGE 5: FINDING #4 - BROKEN PORTAL
# ================================================
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)
page_header(c, 5)

y = H - 65
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 10)
c.drawString(M, y, "FINDING 4")
severity_badge(c, M + 70, y, "BROKEN", RED, RED_LIGHT, RED_BORDER)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 22)
c.drawString(M, y - 30, "Customer Portal Is Dead")

c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 12)
c.drawString(M, y - 55, "Your IVR tells every caller:")
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 12)
c.drawString(M + 175, y - 55, '"Visit MyIWS.com to manage your account."')

c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 12)
c.drawString(M, y - 73, "That domain is for sale.")

c.setStrokeColor(BORDER)
c.line(M, y - 90, W - M, y - 90)

# URL test results
y_table = y - 110
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 13)
c.drawString(M, y_table, "Portal Test Results")

urls = [
    ("myiws.com", "FOR SALE ($2,695)", RED),
    ("interstatewaste.com/myiws", "404 NOT FOUND", RED),
    ("interstatewaste.com/make-a-payment", "404 NOT FOUND", RED),
    ("interstatewaste.com/customer-portal", "404 NOT FOUND", RED),
]

y_url = y_table - 28
for url, status, color in urls:
    draw_rounded_rect(c, M, y_url - 3, W - 2 * M, 26, 4, LIGHT_BG, BORDER)

    c.setFillColor(TEXT_SECONDARY)
    c.setFont('Courier', 9)
    c.drawString(M + 12, y_url + 3, url)

    c.setFillColor(MUTED)
    c.setFont('Helvetica', 10)
    c.drawString(320, y_url + 3, ">")

    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(335, y_url + 3, status)

    y_url -= 32

# What your team says
y_team = y_url - 20
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 13)
c.drawString(M, y_team, "What Your Team Tells Customers")

team_items = [
    ("IVR:", '"Use the MyIWS portal on our website"'),
    ("Rep Charlene:", '"Try BuildTrust"'),
    ("FAQ page:", 'Has a typo: "interstwaste.com"'),
]

y_ti = y_team - 26
for label, detail in team_items:
    draw_rounded_rect(c, M, y_ti - 3, W - 2 * M, 24, 4, BG, BORDER)
    c.setFillColor(TEXT)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(M + 12, y_ti + 3, label)
    lw = c.stringWidth(label, 'Helvetica-Bold', 9)
    c.setFillColor(TEXT_SECONDARY)
    c.setFont('Helvetica', 9)
    c.drawString(M + 12 + lw + 8, y_ti + 3, detail)
    y_ti -= 30

# Pull stat
y_pull = y_ti - 25
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 15)
c.drawCentredString(W / 2, y_pull, "Your customers are told to pay online.")
c.setFillColor(RED)
c.setFont('Helvetica-Bold', 15)
c.drawCentredString(W / 2, y_pull - 24, "There is nowhere to pay online.")

page_footer(c)
c.showPage()


# ================================================
# PAGE 6: THE COST
# ================================================
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)
page_header(c, 6)

# Big number centered
c.setFillColor(RED)
c.setFont('Helvetica-Bold', 72)
c.drawCentredString(W / 2, H / 2 + 100, "$4.8M+")

c.setFillColor(TEXT)
c.setFont('Helvetica', 16)
c.drawCentredString(W / 2, H / 2 + 65, "Estimated Annual AR at Risk")

# Divider
c.setStrokeColor(BORDER)
c.line(W / 2 - 80, H / 2 + 48, W / 2 + 80, H / 2 + 48)

# Breakdown
breakdown = [
    "10,000+ commercial customers across the Northeast",
    "No online payment option available",
    "13.5 hours of daily coverage gap (billing closes 6 PM ET)",
    "48% of payments occur after 6 PM (based on 6,435-payment dataset)",
    "Zero dispute resolution capability at billing level",
    "Customer portal domain is for sale",
]

y_bd = H / 2 + 15
for item in breakdown:
    c.setFillColor(RED)
    c.setFont('Helvetica', 8)
    c.drawString(W / 2 - 195, y_bd + 2, "--")
    c.setFillColor(TEXT_SECONDARY)
    c.setFont('Helvetica', 11)
    c.drawString(W / 2 - 178, y_bd, item)
    y_bd -= 24

# Bottom box
y_bs = y_bd - 35
draw_rounded_rect(c, 120, y_bs, W - 240, 42, 8, RED_LIGHT, RED_BORDER)
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 13)
c.drawCentredString(W / 2, y_bs + 22, "Your billing team disclosed $48,124")
c.drawCentredString(W / 2, y_bs + 6, "and collected $0.")

page_footer(c)
c.showPage()


# ================================================
# PAGE 7: NEXT STEPS
# ================================================
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)
page_header(c, 7)

y = H - 70
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 24)
c.drawString(M, y, "Hear the Full Recordings")

c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 13)
c.drawString(M, y - 28, "This audit includes 3 recorded calls totaling 35 minutes.")
c.drawString(M, y - 46, "Transcripts are synced word-by-word with audio playback.")

# Link card
y_link = y - 90
draw_rounded_rect(c, M, y_link, W - 2 * M, 80, 10, BLUE_LIGHT, HexColor('#C7D2FE'))

# Left accent
c.setFillColor(BLUE)
c.rect(M, y_link, 5, 80, fill=1, stroke=0)

c.setFillColor(BLUE)
c.setFont('Helvetica-Bold', 10)
c.drawString(M + 20, y_link + 58, "INTERACTIVE AUDIT WITH FULL AUDIO")

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 20)
c.drawString(M + 20, y_link + 28, "agentcollect.com/audit-iws")

c.setFillColor(TEXT_SECONDARY)
c.setFont('Helvetica', 10)
c.drawString(M + 20, y_link + 10, "Listen to the calls. Hear your reps. See the evidence.")

# Features list
y_feat = y_link - 30
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 12)
c.drawString(M, y_feat, "On the interactive page:")

features = [
    "Synced audio player with word-by-word transcript highlighting",
    "Jump-to-moment buttons for key findings",
    "Second call recording confirming the pattern",
    "Billing dispute call recording",
    "Live revenue counter showing estimated losses",
]

y_f = y_feat - 22
for feat in features:
    c.setFillColor(BLUE)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(M + 8, y_f + 1, "+")
    c.setFillColor(TEXT_SECONDARY)
    c.setFont('Helvetica', 10)
    c.drawString(M + 22, y_f, feat)
    y_f -= 20

# Divider
c.setStrokeColor(BORDER)
c.line(M, y_f - 10, W - M, y_f - 10)

# Contact section
y_c = y_f - 40
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 16)
c.drawString(M, y_c, "15 minutes to walk you through")
c.drawString(M, y_c - 22, "the full findings.")

# Contact card
y_cc = y_c - 65
draw_rounded_rect(c, M, y_cc, W - 2 * M, 55, 8, LIGHT_BG, BORDER)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 13)
c.drawString(M + 16, y_cc + 32, "John Banner")
c.setFillColor(MUTED)
c.setFont('Helvetica', 10)
c.drawString(M + 16, y_cc + 15, "Founder, AgentCollect (YC S23)")

c.setFillColor(BLUE)
c.setFont('Helvetica', 10)
c.drawString(M + 16, y_cc + 1, "j@agentcollect.com")
c.setFillColor(MUTED)
c.drawString(M + 180, y_cc + 1, "(415) 867-4010")

# Footer
c.setStrokeColor(BORDER)
c.line(M, 70, W - M, 70)
c.setFillColor(LIGHT_MUTED)
c.setFont('Helvetica', 8)
c.drawCentredString(W / 2, 55, "This audit was conducted April 2026 using publicly available information and recorded phone calls.")
c.drawCentredString(W / 2, 43, "All findings are based on direct observation. No data was fabricated.")

c.showPage()

# Save
c.save()
print(f"PDF saved to {OUT}")
print(f"Size: {os.path.getsize(OUT):,} bytes")
