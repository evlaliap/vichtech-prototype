import streamlit as st

st.set_page_config(page_title="VIChTech Prototype", layout="wide")

st.markdown(
    """
<style>
html, body, [class*="css"], button, input, textarea, select { font-family: Arial, Helvetica, sans-serif !important; }
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stToolbarActions"], [data-testid="stAppDeployButton"] { display: none; }
.block-container { padding-top: 4rem; }
button, input, textarea, [data-baseweb], [data-baseweb] > div, .stTextInput *, .stNumberInput *, .stSelectbox *, .stTextArea * { border-radius: 0 !important; }
.stTextInput [data-baseweb="input"], .stNumberInput [data-baseweb="input"], .stSelectbox [data-baseweb="select"] > div, .stTextArea [data-baseweb="textarea"] { border: 1px solid #999999 !important; background: #ffffff !important; }
.stTextInput input, .stNumberInput input, .stTextArea textarea { background: #ffffff !important; }
div.stButton > button { border: 1px solid #1f5aa6; color: #1f5aa6; background: #ffffff; font-weight: bold; }
div.stButton > button[kind="primary"] { background: #1f5aa6; color: #ffffff; }
section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #cccccc; }
section[data-testid="stSidebar"] div.stButton > button { border: 0; border-bottom: 1px solid #eeeeee; color: #1f5aa6;
  font-weight: normal; justify-content: flex-start; text-align: left; padding: 4px 2px; min-height: 0; }
section[data-testid="stSidebar"] div.stButton > button > div { justify-content: flex-start; width: 100%; }
section[data-testid="stSidebar"] div.stButton > button p { text-align: left; }
.st-key-phone div.stButton > button { padding: 6px 2px; min-height: 0; }
.st-key-phone div.stButton > button p { font-size: 13px; }
.st-key-phone [data-testid="stHorizontalBlock"] { gap: 6px; }
.st-key-phone { max-width: 370px; margin: 0 auto; border: 8px solid #111111; border-radius: 18px; padding: 0 14px 14px; background: #ffffff; }
.st-key-console { border: 1px solid #cccccc; padding: 0 16px 16px; background: #ffffff; }
.bar { background: #1f5aa6; color: #ffffff; padding: 12px; margin: 0 -14px 10px; font-size: 16px; font-weight: bold; }
.cbar { background: #444444; color: #ffffff; text-align: center; font-size: 12px; padding: 4px; margin: 0 -14px; }
.box { border: 1px solid #cccccc; background: #f5f5f5; padding: 10px 12px; margin-bottom: 10px; font-size: 14px; }
.box .big { font-size: 26px; font-weight: bold; }
.line { display: flex; justify-content: space-between; gap: 12px; padding: 5px 0; border-bottom: 1px solid #eeeeee; font-size: 14px; }
.line:last-child { border-bottom: 0; }
.line span:first-child { color: #666666; }
.card { border: 1px solid #cccccc; background: #ffffff; padding: 8px 12px; margin-bottom: 10px; }
.muted { color: #666666; font-size: 13px; }
.status { color: #666666; font-size: 12px; font-style: italic; }
.step { color: #666666; font-size: 12px; font-weight: bold; margin-bottom: 6px; }
.hist { border-bottom: 1px dotted #cccccc; padding: 4px 0; font-size: 14px; }
.hist small { display: block; color: #666666; }
.qr { width: 170px; height: 170px; margin: 10px auto; padding: 6px; border: 1px solid #cccccc; }
table.t { width: 100%; border-collapse: collapse; font-size: 13px; }
table.t th, table.t td { border: 1px solid #cccccc; padding: 6px; text-align: left; }
table.t th { background: #f5f5f5; }
.bad { font-weight: bold; text-decoration: underline; }
</style>
""",
    unsafe_allow_html=True,
)

ss = st.session_state



def rs(n):
    """Indian rupee format, e.g. ₹11,48,920.00"""
    whole, dec = f"{abs(n):.2f}".split(".")
    if len(whole) > 3:
        last3, rest, groups = whole[-3:], whole[:-3], []
        while len(rest) > 2:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.insert(0, rest)
        whole = ",".join(groups + [last3])
    return ("-" if n < 0 else "") + "₹" + whole + "." + dec


def h(state, time, note=""):
    return {"state": state, "time": time, "note": note}


def html(text):
    st.markdown(text, unsafe_allow_html=True)


def lines(rows, box="card"):
    html(f'<div class="{box}">' + "".join(f'<div class="line"><span>{a}</span><b>{b}</b></div>' for a, b in rows) + "</div>")


def qr_svg():
    s, out = 7, ""
    for y in range(21):
        for x in range(21):
            corner = (x < 7 and y < 7) or (x > 13 and y < 7) or (x < 7 and y > 13)
            if corner:
                a, b = (x - 14 if x > 13 else x), (y - 14 if y > 13 else y)
                on = a in (0, 6) or b in (0, 6) or (1 < a < 5 and 1 < b < 5)
            else:
                s = (s * 9301 + 49297) % 233280
                on = s / 233280 > 0.5
            if on:
                out += f'<rect x="{x * 8}" y="{y * 8}" width="8" height="8"/>'
    return f'<div class="qr"><svg viewBox="0 0 168 168" width="100%" height="100%">{out}</svg></div>'


#example data (state names match our Sprint 3 state machine diagram)
if "ready" not in ss:
    ss.ready = True
    ss.view = "Mobile app"
    ss.screen = "welcome"
    ss.back = []
    ss.sel = "PAY-48213"
    ss.amount = 450
    ss.flash = ""
    ss.staff = "Compliance officer"
    ss.case_done = False
    ss.support_step = 1
    ss.batch = False
    ss.staff_in = False
    ss.goods_given = False
    ss.case_open = False
    ss.payment_found = False
    ss.user = {"name": "Meena Iyer", "shop": "Meena's Kirana Store", "phone": "+91 98450 21734",
               "email": "meena.kirana@gmail.com", "balance": 18640.50, "tier": "Basic"}
    ss.payments = [
        {"id": "PAY-48213", "who": "Priya Nair", "amount": 450, "incoming": True, "when": "Today, 10:42 am", "state": "Awaiting Settlement",
         "history": [h("Screening", "10:41 am"), h("Authorising", "10:41 am"), h("Capturing", "10:42 am"), h("Awaiting Settlement", "10:42 am", "Batch closes 11:00 pm")]},
        {"id": "PAY-48190", "who": "Hotel Annapoorna", "amount": 12500, "incoming": True, "when": "Today, 9:15 am", "state": "Held for Compliance Review",
         "history": [h("Screening", "9:15 am", "Risk score 74"), h("Held for Compliance Review", "9:15 am")]},
        {"id": "PAY-47766", "who": "Lakshmi Bai", "amount": 2340, "incoming": True, "when": "21 Oct", "state": "Settled",
         "history": [h("Screening", "21 Oct"), h("Authorising", "21 Oct"), h("Capturing", "21 Oct"), h("Awaiting Settlement", "21 Oct"), h("Settling", "21 Oct, 11:00 pm"), h("Settled", "22 Oct, 6:10 am")]},
        {"id": "PAY-47590", "who": "Fresh Dairy Supplies", "amount": 320, "incoming": False, "when": "21 Oct", "state": "Cancelled",
         "history": [h("Screening", "21 Oct"), h("Authorising", "21 Oct"), h("Capturing", "21 Oct"), h("Awaiting Settlement", "21 Oct"), h("Cancelled", "21 Oct", "Money returned")]},
        {"id": "PAY-47411", "who": "Vinod Traders", "amount": 5600, "incoming": True, "when": "20 Oct", "state": "Failed",
         "history": [h("Screening", "20 Oct"), h("Authorising", "20 Oct", "3 attempts failed"), h("Failed", "20 Oct", "No money moved")]},
    ]

user = ss.user


def find(pid):
    return next((p for p in ss.payments if p["id"] == pid), ss.payments[0])


#navigation
def go(screen, sel=None):
    ss.back.append(ss.screen)
    ss.screen = screen
    if sel:
        ss.sel = sel


def go_back():
    if ss.back:
        ss.screen = ss.back.pop()


def tab(screen):
    ss.back = []
    ss.screen = screen


# actions
def show_qr():
    ss.amount = ss.sale_amount
    go("qr")


def customer_paid():
    # Check the balance and tier limits (include in UC34)
    if ss.amount > 2310 or ss.amount > 10000:
        ss.flash = "Payment blocked: not enough balance or over the Basic tier limit of ₹10,000. No money moved."
        return
    user["balance"] += ss.amount
    ss.last_id = f"PAY-{48225 + len(ss.payments)}"
    ss.payments.insert(0, {"id": ss.last_id, "who": "Priya Nair", "amount": ss.amount, "incoming": True, "when": "Just now", "state": "Awaiting Settlement",
                           "history": [h("Screening", "Just now"), h("Authorising", "Just now", "Priya confirmed"), h("Capturing", "Just now"),
                                       h("Awaiting Settlement", "Just now", "Batch closes 11:00 pm")]})
    ss.goods_given = False
    ss.back = []
    ss.screen = "received"


def customer_cancel():
    tab("home")
    ss.flash = "Customer cancelled. Nothing was charged."


def pay_now():
    if ss.pay_amount > 10000:
        ss.flash = "Over your tier limit of ₹10,000."
        return
    user["balance"] -= ss.pay_amount
    ss.payments.insert(0, {"id": f"PAY-{48225 + len(ss.payments)}", "who": ss.pay_to, "amount": ss.pay_amount, "incoming": False,
                           "when": "Just now", "state": "Awaiting Settlement",
                           "history": [h("Screening", "Just now"), h("Authorising", "Just now", "You confirmed"),
                                       h("Capturing", "Just now"), h("Awaiting Settlement", "Just now")]})
    tab("home")
    ss.flash = "Payment sent."


def top_up():
    user["balance"] += ss.topup_amount
    tab("home")
    ss.flash = "Money added from HDFC Bank."


def cancel_payment():
    p = find(ss.sel)
    if p["state"] == "Awaiting Settlement":
        user["balance"] += -p["amount"] if p["incoming"] else p["amount"]
    p["state"] = "Cancelled"
    p["history"].append(h("Cancelled", "Just now", "Money returned to the payer"))
    ss.flash = "Payment cancelled."


def save_profile():
    user["shop"], user["email"], user["phone"] = ss.edit_shop, ss.edit_email, ss.edit_phone
    go_back()
    ss.flash = "Profile updated."


def set_flag(name, value):
    ss[name] = value


def set_flash(msg):
    ss.flash = msg


# sidebar: use case list
USE_CASES = [
    ("Register an account", "Mobile app", "reg1"),
    ("Manage the profile", "Mobile app", "profile"),
    ("Accept a customer payment", "Mobile app", "charge"),
    ("Make a payment", "Mobile app", "pay"),
    ("Top up the wallet", "Mobile app", "topup"),
    ("View the transaction history", "Mobile app", "payments"),
    ("Cancel a payment", "Mobile app", "detail"),
    ("View the notification history", "Mobile app", "inbox"),
    ("Review a flagged verification case", "Staff console", "Compliance officer"),
    ("Run the daily settlement", "Staff console", "Administrator"),
    ("Resolve a failed payment", "Staff console", "Support officer"),
    ("View the executive dashboard", "Staff console", "Executive"),
]


def jump(view, target):
    ss.view = view
    ss.flash = ""
    if view == "Mobile app":
        ss.back = ["welcome"] if target == "reg1" else ["home"]
        ss.screen = target
        if target == "detail":
            ss.sel = "PAY-48213"
    else:
        ss.staff = target
        ss.staff_in = True


with st.sidebar:
    st.markdown("### Use cases")
    st.caption("Click a use case to open it.")
    for i, (name, view, target) in enumerate(USE_CASES):
        st.button(name, key=f"uc{i}", on_click=jump, args=(view, target), use_container_width=True)

# top bar
st.markdown("## VIChTech")
st.radio("View", ["Mobile app", "Staff console"], key="view", horizontal=True, label_visibility="collapsed")


#  mobile screens 
def header(title, can_back=True):
    html(f'<div class="bar">{title}</div>')
    if can_back:
        st.button("‹ Back", key="back_btn", on_click=go_back)


def bottom_nav(active):
    cols = st.columns(4)
    for col, (screen, label) in zip(cols, [("home", "Home"), ("payments", "Payments"), ("inbox", "Inbox"), ("profile", "Profile")]):
        col.button(label, key=f"nav_{screen}", on_click=tab, args=(screen,), use_container_width=True,
                   type="primary" if screen == active else "secondary")


def payment_row(p):
    left, right = st.columns([3, 2])
    sign = "+" if p["incoming"] else "-"
    left.markdown(f"**{p['who']}**  \n<span class='muted'>{p['when']}</span>  \n<span class='status'>Status: {p['state']}</span>", unsafe_allow_html=True)
    right.markdown(f"**{sign}{rs(p['amount'])}**")
    right.button("View", key=f"view_{p['id']}", on_click=go, args=("detail", p["id"]))


def screen_welcome():
    html('<div class="bar">VIChTech</div>')
    st.markdown("### Welcome to VIChTech")
    html('<p class="muted">Take payments and manage your wallet.</p>')
    st.button("Create an account", type="primary", use_container_width=True, on_click=go, args=("reg1",))
    st.button("Sign in", use_container_width=True, on_click=go, args=("signin",))


def screen_signin():
    header("Sign in")
    st.text_input("Mobile number", value=user["phone"], key="si_phone")
    st.text_input("Password", value="password", type="password", key="si_pw")
    st.text_input("One-time passcode", value="482913", key="si_otp")
    st.button("Sign in", type="primary", use_container_width=True, on_click=tab, args=("home",))


# Register an account (UC01)
def screen_reg1():
    header("Create an account")
    html('<div class="step">Step 1 of 3 · Contact details</div>')
    st.text_input("Mobile number", value=user["phone"], key="r_phone")
    st.text_input("Email", value=user["email"], key="r_email")
    st.text_input("Passcode sent to your phone", value="482913", key="r_otp")
    html('<p class="muted">3 attempts allowed.</p>')
    st.button("Confirm", type="primary", use_container_width=True, on_click=go, args=("reg2",))


def screen_reg2():
    header("Your details")
    html('<div class="step">Step 2 of 3 · Details and documents</div>')
    html('<div class="box">Number confirmed. Your account is created but not verified yet.</div>')
    st.selectbox("Account type", ["Micro merchant", "Freelancer", "Gig worker"], key="r_type")
    st.text_input("Full name", value=user["name"], key="r_name")
    st.text_input("Business name", value=user["shop"], key="r_shop")
    st.selectbox("Expected money each month", ["Up to ₹50,000 (Basic tier)", "More than ₹50,000 (Full tier)"], key="r_tier")
    st.button("Upload photo ID", use_container_width=True, on_click=set_flash, args=("Aadhaar card uploaded.",))
    st.button("Take a selfie", use_container_width=True, on_click=set_flash, args=("Selfie recorded.",))
    st.button("Send for checking", type="primary", use_container_width=True, on_click=go, args=("reg3",))


def screen_reg3():
    header("Account active", can_back=False)
    html('<div class="step">Step 3 of 3 · Verification</div>')
    lines([("Document checked", "Done"), ("Selfie matched to ID", "Done"), ("Sanctions screening", "Done"), ("Wallet opened (Basic tier)", "Done")])
    html('<div class="box">Your account is active. A welcome message has been sent.</div>')
    st.button("Sign in", type="primary", use_container_width=True, on_click=go, args=("signin",))


def screen_home():
    header("Home", can_back=False)
    html(f'<p class="muted">Hello {user["name"].split()[0]} · {user["shop"]}</p>')
    html(f'<div class="box"><span class="muted">Wallet balance</span><div class="big">{rs(user["balance"])}</div>'
         f'<span class="muted">{user["tier"]} tier · up to ₹10,000 a payment</span></div>')
    c1, c2, c3 = st.columns(3)
    c1.button("Charge", use_container_width=True, on_click=go, args=("charge",))
    c2.button("Pay", use_container_width=True, on_click=go, args=("pay",))
    c3.button("Top up", use_container_width=True, on_click=go, args=("topup",))
    st.markdown("**Recent payments**")
    for p in ss.payments[:3]:
        payment_row(p)
    bottom_nav("home")


# Accept a customer payment (UC34)
def screen_charge():
    header("Charge a customer")
    html('<div class="box">Your account is active and verified.</div>')
    st.number_input("Sale amount (₹)", min_value=1, value=int(ss.amount), step=10, key="sale_amount")
    st.button("Show QR code", type="primary", use_container_width=True, on_click=show_qr)


def screen_qr():
    header("Customer scans to pay")
    html(f'<p class="muted" style="text-align:center">{user["shop"]}</p>'
         f'<p style="text-align:center;font-size:26px;font-weight:bold;margin:0">{rs(ss.amount)}</p>{qr_svg()}'
         f'<p class="muted" style="text-align:center">Expires in 5 minutes</p>')
    st.button("Show customer's phone", type="primary", use_container_width=True, on_click=go, args=("customer",))


def screen_customer():
    html('<div class="cbar">Customer\'s phone (Priya Nair)</div><div class="bar">Confirm payment</div>')
    lines([("Pay to", user["shop"]), ("Amount", rs(ss.amount)), ("Your balance", rs(2310))])
    st.button("Confirm and pay", type="primary", use_container_width=True, on_click=customer_paid)
    st.button("Cancel", use_container_width=True, on_click=customer_cancel)


def screen_received():
    header("Payment received", can_back=False)
    html(f'<p style="font-size:18px;font-weight:bold;margin:6px 0 0">Payment received</p>'
         f'<p style="font-size:26px;font-weight:bold;margin:0">+{rs(ss.amount)}</p><p class="muted">From Priya Nair</p>'
         '<div class="box">Balance and tier limit checked. Receipt sent to Priya. Sound alert played on your phone.</div>')
    if not ss.goods_given:
        st.button("Goods handed over", type="primary", use_container_width=True, on_click=set_flag, args=("goods_given", True))
    else:
        html('<div class="box">Sale complete. The payment is in today\'s settlement batch (closes 11:00 pm).</div>')
        st.button("View payment", type="primary", use_container_width=True, on_click=go, args=("detail", ss.last_id))
        st.button("Done", use_container_width=True, on_click=tab, args=("home",))


def screen_pay():
    header("Make a payment")
    st.selectbox("Pay to", ["Sharma Medicals", "Fresh Dairy Supplies"], key="pay_to")
    st.number_input("Amount (₹)", min_value=1, value=760, step=10, key="pay_amount")
    st.button("Pay now", type="primary", use_container_width=True, on_click=pay_now)


def screen_topup():
    header("Top up wallet")
    st.number_input("Amount (₹)", min_value=1, value=2000, step=100, key="topup_amount")
    lines([("From", "HDFC Bank •••• 4821")])
    st.button("Top up", type="primary", use_container_width=True, on_click=top_up)


def screen_payments():
    header("Payments", can_back=False)
    for p in ss.payments:
        payment_row(p)
        html('<hr style="margin:4px 0;border:0;border-top:1px solid #cccccc">')
    bottom_nav("payments")


# Payment details: shows the states from the state machine diagram
def screen_detail():
    p = find(ss.sel)
    header("Payment details")
    lines([("From" if p["incoming"] else "To", p["who"]), ("Amount", rs(p["amount"])), ("Reference", p["id"]), ("Status", p["state"])])
    html('<div class="card"><b>Payment status</b>' + "".join(
        f'<div class="hist"><b>{x["state"]}</b><small>{x["time"]}{" · " + x["note"] if x["note"] else ""}</small></div>' for x in p["history"]) + "</div>")
    if p["state"] in ("Screening", "Held for Compliance Review", "Authorising", "Awaiting Settlement"):
        st.button("Cancel this payment", use_container_width=True, on_click=cancel_payment)
        html('<p class="muted" style="text-align:center">You can cancel until the batch closes.</p>')


def screen_inbox():
    header("Inbox", can_back=False)
    html('<div class="card">'
         '<div class="hist"><b>Payment received</b><small>Priya Nair paid you ₹450.00</small></div>'
         '<div class="hist"><b>New sign-in on another phone</b><small>Security alert</small></div>'
         '<div class="hist"><b>Takings paid to your bank</b><small>₹7,812.40 sent to HDFC Bank</small></div></div>')
    st.markdown("**Send me messages by**")
    st.checkbox("Push", value=True, key="n_push")
    st.checkbox("SMS", value=True, key="n_sms")
    st.checkbox("Email", value=False, key="n_email")
    html('<p class="muted">Security alerts are always sent.</p>')
    bottom_nav("inbox")


def screen_profile():
    header("Profile", can_back=False)
    lines([("Name", user["name"]), ("Business", user["shop"]), ("Mobile", user["phone"]), ("Email", user["email"]), ("Tier", user["tier"])])
    st.button("Edit profile", type="primary", use_container_width=True, on_click=go, args=("edit",))
    st.button("Sign out", use_container_width=True, on_click=tab, args=("welcome",))
    bottom_nav("profile")


def screen_edit():
    header("Edit profile")
    st.text_input("Business name", value=user["shop"], key="edit_shop")
    st.text_input("Email", value=user["email"], key="edit_email")
    st.text_input("Mobile", value=user["phone"], key="edit_phone")
    st.button("Save changes", type="primary", use_container_width=True, on_click=save_profile)


SCREENS = {
    "welcome": screen_welcome, "signin": screen_signin, "reg1": screen_reg1, "reg2": screen_reg2, "reg3": screen_reg3,
    "home": screen_home, "charge": screen_charge, "qr": screen_qr, "customer": screen_customer, "received": screen_received,
    "pay": screen_pay, "topup": screen_topup, "payments": screen_payments, "detail": screen_detail,
    "inbox": screen_inbox, "profile": screen_profile, "edit": screen_edit,
}


# staff console 
def staff_case():
    if not ss.case_open:
        st.markdown("#### Verification queue")
        html('<p class="muted">Cases the automatic checks could not decide. Oldest first.</p>')
        html('<table class="t"><tr><th>Case</th><th>Applicant</th><th>Why it is here</th><th>Waiting</th></tr>'
             '<tr><td>VC-2291</td><td>Meena Iyer</td><td>Selfie match not clear</td><td><b>2 days (overdue)</b></td></tr>'
             '<tr><td>VC-2298</td><td>Farhan Siddiqui</td><td>Possible sanctions list match</td><td>1 day</td></tr>'
             '<tr><td>VC-2304</td><td>Deepa Krishnan</td><td>Address does not match ID</td><td>4 hours</td></tr></table>')
        st.write("")
        st.button("Open oldest case (VC-2291)", type="primary", on_click=set_flag, args=("case_open", True))
        return
    st.markdown("#### Verification case VC-2291")
    html('<p class="muted">Meena Iyer · micro merchant · selfie match not clear · waiting 2 days</p>')
    a, b = st.columns(2)
    a.markdown('<div class="card"><b>Application against ID</b><table class="t" style="margin-top:6px"><tr><th>Field</th><th>Entered</th><th>On ID</th></tr>'
               '<tr><td>Name</td><td>Meena Iyer</td><td>Meena Iyer</td></tr>'
               '<tr><td>Date of birth</td><td>12/04/1984</td><td>12/04/1984</td></tr>'
               '<tr><td>Address</td><td>Jayanagar</td><td class="bad">Basavanagudi</td></tr></table></div>', unsafe_allow_html=True)
    with b:
        st.markdown("**Checks**")
        lines([("Face match", "71% (pass 85%)"), ("Risk tier", "Basic")])
        st.markdown("**Screening hit**")
        lines([("List entry", "Meena R. Iyer, PEP list"), ("Why it matched", "Same first and last name"),
               ("How close", "62%, born 1971 (not 1984)")])
    if ss.case_done:
        html('<div class="box">Approved. Audit log written and the applicant has been told.</div>')
    else:
        st.text_input("Reason", value="Old address on ID. Screening hit is a different person.", key="case_reason")
        c1, c2 = st.columns(2)
        c1.button("Approve", type="primary", use_container_width=True, on_click=set_flag, args=("case_done", True))
        c2.button("Decline", use_container_width=True, on_click=set_flash, args=("Application declined.",))
        c3, c4 = st.columns(2)
        c3.button("Request additional documents", use_container_width=True, on_click=set_flash, args=("Documents requested.",))
        c4.button("Report a suspicious matter", use_container_width=True, on_click=set_flash,
                  args=("Suspicious matter report started. The applicant is not told.",))


def close_batch():
    """[t = daily settlement cut-off] / add to batch, submit to partner bank"""
    for p in ss.payments:
        if p["state"] == "Awaiting Settlement":
            p["state"] = "Settling"
            p["history"].append(h("Settling", "Just now", "Sent to HDFC Bank"))
    ss.batch = True


def staff_settle():
    st.markdown("#### Daily settlement")
    html('<p class="muted">Batch for today · cut-off 11:00 pm</p>')
    waiting = [p for p in ss.payments if p["state"] == "Awaiting Settlement"]
    rows = "".join(f'<tr><td>{p["id"]}</td><td>{p["who"]}</td><td>{rs(p["amount"])}</td><td>{p["state"]}</td></tr>' for p in waiting)
    if waiting:
        html('<table class="t"><tr><th>Reference</th><th>With</th><th>Amount</th><th>Status</th></tr>' + rows + '</table>')
    else:
        html('<p class="muted">No payments are waiting for settlement.</p>')
    if ss.batch:
        html('<div class="box" style="margin-top:10px">Batch sent to HDFC Bank. The payments moved from Awaiting Settlement to Settling. '
             'If the bank rejects a transfer it is retried on the next run, up to 3 times, then the payment Fails.</div>')
    else:
        st.write("")
        st.button("Close batch and send to bank", type="primary", on_click=close_batch, disabled=not waiting)


def staff_support():
    st.markdown("#### Case SUP-1204 · charged twice")
    if not ss.payment_found:
        html('<p class="muted">Anil Shetty says he was charged twice for one order at Sharma Medicals.</p>')
        st.text_input("Payment reference", value="PAY-48140", key="support_ref")
        st.button("Find payment", type="primary", on_click=set_flag, args=("payment_found", True))
        return
    states = ["Settled", "Reversing", "Reversed", "Reversed"]
    html(f'<p class="muted">Payment PAY-48140 · Anil Shetty to Sharma Medicals · {rs(640)}</p>')
    a, b = st.columns(2)
    a.markdown('<div class="card"><b>Wallet movements</b><table class="t" style="margin-top:6px">'
               f'<tr><td>Anil Shetty</td><td>-{rs(640)}</td><td>PAY-48139</td></tr>'
               f'<tr><td>Anil Shetty</td><td class="bad">-{rs(640)}</td><td>PAY-48140</td></tr>'
               f'<tr><td>Sharma Medicals</td><td>+{rs(640)}</td><td>both</td></tr></table></div>', unsafe_allow_html=True)
    b.markdown(f'<div class="card"><b>Status</b><br><span class="status">Status: {states[ss.support_step - 1]}</span>'
               '<p class="muted">Last step: Settled. No bank error.</p></div>', unsafe_allow_html=True)
    lines([("Settlement", "Batch 22 Oct, paid to Sharma Medicals 23 Oct"),
           ("Notifications", "Receipt sent to Anil 22 Oct, 7:59 pm (delivered)")])
    step = ss.support_step
    if step == 1:
        c1, c2, c3 = st.columns(3)
        c1.button("Reverse a payment", type="primary", on_click=set_flag, args=("support_step", 2))
        c2.button("Complete", on_click=set_flash, args=("Payment completed.",))
        c3.button("Explain", on_click=set_flash, args=("Explanation sent.",))
    elif step == 2:
        html('<div class="box">Reversal opened. Waiting for the bank to return the money.</div>')
        st.button("Bank returned the money", type="primary", on_click=set_flag, args=("support_step", 3))
    elif step == 3:
        html(f'<div class="box">{rs(640)} returned to Anil.</div>')
        st.text_area("Message to Anil", value="Hi Anil, you were charged twice for one order. We have returned ₹640.00 to your wallet.",
                     key="support_msg")
        st.button("Send message and close case", type="primary", on_click=set_flag, args=("support_step", 4))
    else:
        html('<div class="box">Case closed. Audit log written and Anil has been sent the message.</div>')


def staff_exec():
    st.markdown("#### Executive dashboard")
    html('<p class="muted">October 2026</p>')
    cols = st.columns(4)
    for col, (label, value) in zip(cols, [("Registrations", "3,412"), ("Verified", "2,906"), ("Volume", "₹2.86 cr"), ("Failure rate", "1.4%")]):
        col.markdown(f'<div class="card"><span class="muted">{label}</span><br><b style="font-size:18px">{value}</b></div>', unsafe_allow_html=True)
    st.markdown("**Revenue by payment type**")
    lines([("Collections (pull)", "₹2,19,800 commission"), ("Disbursements (push)", "₹33,300 commission")])
    report = "Measure,Value\nRegistrations,3412\nVerified,2906\nPayment volume (INR),28600000\nFailure rate,1.4%\n" \
             "Commission collections (INR),219800\nCommission disbursements (INR),33300\n"
    st.download_button("Export a report (CSV)", report, file_name="vichtech_report.csv", type="primary")


STAFF = {"Compliance officer": staff_case, "Administrator": staff_settle, "Support officer": staff_support, "Executive": staff_exec}

# staff sign in (the real system checks the password and the one-time code, the prototype does not)
STAFF_PEOPLE = {
    "Compliance officer": ("Kavya Menon", "kavya.menon@vichtech.in"),
    "Administrator": ("Neha Joshi", "neha.joshi@vichtech.in"),
    "Support officer": ("Rohit Shah", "rohit.shah@vichtech.in"),
    "Executive": ("Vikram Patel", "vikram.patel@vichtech.in"),
}


def staff_sign_in():
    ss.staff = ss.login_role
    ss.staff_in = True


def staff_sign_out():
    ss.staff_in = False


def staff_login():
    st.markdown("#### Staff sign in")
    html('<p class="muted">Only VIChTech staff can use the staff console. Each role only sees its own screens.</p>')
    role = st.selectbox("Role", list(STAFF), key="login_role")
    st.text_input("Work email", value=STAFF_PEOPLE[role][1], key=f"login_email_{role}")
    st.text_input("Password", value="password", type="password", key="login_pw")
    st.text_input("One-time code sent to your phone", value="736201", key="login_otp")
    html('<p class="muted">Prototype: the details are filled in so the marker can sign in.</p>')
    st.button("Sign in", type="primary", on_click=staff_sign_in)


# drawing the page
if ss.view == "Mobile app":
    _, middle, _ = st.columns([1, 1.4, 1])
    with middle:
        with st.container(key="phone"):
            SCREENS[ss.screen]()
            if ss.flash:
                html(f'<div class="box">{ss.flash}</div>')
                ss.flash = ""
else:
    with st.container(key="console"):
        if not ss.staff_in:
            staff_login()
        else:
            name = STAFF_PEOPLE[ss.staff][0]
            left, right = st.columns([4, 1])
            left.markdown(f'<p class="muted" style="margin-top:8px">Signed in as <b>{name}</b> · {ss.staff}</p>', unsafe_allow_html=True)
            right.button("Sign out", on_click=staff_sign_out, use_container_width=True)
            STAFF[ss.staff]()
            if ss.flash:
                html(f'<div class="box">{ss.flash}</div>')
                ss.flash = ""
