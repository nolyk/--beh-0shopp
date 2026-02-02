class Language:
    def __init__(self):
        self.language = "en"
    
    class Buttons:
        buy = "💸 Buy"
        profile = "👤 Profile"
        support = "💎 Support"
        faq = "❓ FAQ"
        topup_balance = "💰 Topup balance"
        back = "◀ Back"
        contests = "🎁 Giveaways"
        faq_chat_inl = "💎 Chat"
        faq_news_inl = "📩 News"

        #  Inline
        send_payment_to_check = "✅ Send payment for verification"
        close = "❌ Close"
        activate_promo = "📢 Activate promocode"
        ref_system = "👥 Referral system"
        purchases_history = "🛒 Purchases history"
        support_text = "🔗 Write to support"
        refill_link_inl = "💵 Proceed to payment"
        refill_check_inl = "💎 Check payment"
        cancel = "❌ Cancel"
        admin_panel = "⚙ Admin Panel"
        choose_action = "Select action"
        position_button_name = "{name} | {price}{curr} | {items}"
        nolimit = "Unlimited"
        pcs = "pcs."
        contest_enter = '🎉 Participate'
        you_not_completed_all_conditions = "❗ You have not fulfilled all the conditions! {count} of {count_conditions} fulfilled"
        change_language = "🌐 Change language"
        check_sub = "✅ Check"
        

    class Texts:

        #######################################
        #  Min/Max Amount of refill (IN uzs)  #
        #                                     #
        min_amount = 5                        #
        max_amount = 100000                   #
        #                                     #
        #                                     #
        #######################################

        is_buy_text = "❌ Shopping is temporarily unavailable!"
        is_ban_text = f"❌ You have been blocked in the bot!"
        is_work_text = f"❌ The bot is undergoing maintenance work.!"
        is_refill_text = f"❌ Top-ups are temporarily unavailable!"
        is_ref_text = f"❌ The referral system is temporarily unavailable.!"
        is_contests_text = f"❌ Giveaways are temporarily unavailable!"
        channels_error = """
<b>❌ Error!\n\nYou have not subscribed to all channels:

{urls_txt}</b>
    """

        nobody = "<code>Nobody</code>"
        ref_s = ('referral', 'referrals', 'referrals')
        day_s = ('day', 'days', "days")
        member_s = ("member", "members", "members")
        winner_s = ("winner", "winners", "winners")
        refill_s = ("replenishment", "replenishments", "replenishments") 
        purchase_s = ("purchase", "purchases", "purchases") 
        channel_s = ('channel', 'channels', 'channels')
        person_s = ('person', "persons", "persons")

        main_menu = """
<b>👩‍💻 {username}, Thank you for using our Store

Main menu:</b>"""
        bot_will_not_respond = "❗ The bot will not respond until the spam stops."
        please_dont_spam = "❗ Please do not spam."
        
        profile_text = """
<b>👤 Your profile:

💎 User: {username}
🆔 ID: <code>{user_id}</code>

💰 Balane: <code>{balance}{curr}</code>
💵 Total replenished: <code>{total_refill}{curr}</code>

📌 Registration date: <code>{reg_date}</code></b>"""
        support_is_not_provided = "<b>💎 There is currently no current support.!</b>"
        support_text = "<b>💎 To write to support, click on the button below:</b>"
        choose_language = "<b>❗ Выберите язык / Choose language:</b>"
        refill_check_no = "❌ Payment not found"
        payments_names = {
            "lolz": "💚 Lolzteam",
            "payok": "🟡 PayOK",
            "aaio": "💳 Aaio",
            'yoomoney': "🟣 ЮMoney",
            'lava': "⭐ Lava",
            'cryptoBot': "💡 CryptoBot",
            'crystalPay': "💎 CrystalPay",
            'cryptomus': "🖤 Cryptomus"
        }
        choose_refill_method = "<b>💰 Select replenishment method:</b>"
        payment_comment_api = "Top up account {user_name} with the amount {pay_amount}{curr} in the @{bot_name} bot"
        refill_was_rejected = "<b>❌ Your replenishment of {amount}{curr} was declined!</b>"
        send_receipt_photo = "<b>🧾 Send a photo of the transfer receipt:</b>"
        confirm_send_receipt_photo = "<b>❓ Are you sure you want to submit this check for verification??</b>"
        create_refill_text = """
<b>⭐ Replenishment via: <code>{paymentMethod}</code>
💰 Amount: <code>{pay_amount}{curr}</code>
🆔 Payment ID: <code>{pay_id}</code>
⌛ You must pay the bill before <code>{under_date}</code>
💎 To pay, click the button below:</b>"""
        cancel_create_refill_text = """
<b>❗ You already have an active replenishment:

⭐ Replenishment via: <code>{paymentMethod}</code>
💰 Amount: <code>{pay_amount}{curr}</code>
🆔 Payment ID: <code>{pay_id}</code>
⌛ You must pay the bill before <code>{under_date}</code>
💎 To pay, click the button below:</b>"""
        create_refill_text_custom_pay_method = """
<b>⭐ Replenishment via: <code>{paymentMethod}</code>
💰 Amount: <code>{pay_amount}{curr}</code>
🆔 Payment ID: <code>{pay_id}</code>
⌛ You must pay the bill before <code>{under_date}</code></b>

{custom_pay_method_text}"""
        cancel_create_refill_text_custom_pay_method = """
<b>❗ You already have an active replenishment:

⭐ Replenishment via: <code>{paymentMethod}</code>
💰 Amount: <code>{pay_amount}{curr}</code>
🆔 Payment ID: <code>{pay_id}</code>
⌛ You must pay the bill before <code>{under_date}</code></b>

{custom_pay_method_text}"""
        enter_amount_of_refill = "<b>❗ Enter the top-up amount:</b>"
        choose_crypto = "<b>⚙️ Select cryptocurrency:</b>"
        error_refill = "❌ Error, replenishment has already occurred!"
        success_refill_text = """
<b>⭐ You have successfully topped up your balance with the amount <code>{amount}{curr}</code>
💎 Pay method: <code>{way}</code>
🧾 Receipt: <code>{receipt}</code></b>
"""
        yes_refill_ref = "<b>💎 Your referral {name} topped up their balance by <code>{amount}{cur}</code> and you were credited with <code>{ref_amount}{cur}</code></b>"
        yes_cancel_refill = "<b>❌ Replenishment canceled</b>"
        no_int_amount = "<b>❗ The replenishment amount must be a number!</b>"
        min_max_amount = "<b>❗ The replenishment amount must be greater than or equal to <code>{min_amount}{curr}</code> but less than or equal to <code>{max_amount}{curr}</code></b>"
        new_ref_lvl = "<b>💚 You have a new referral level, {new_lvl}! There are {next_lvl} levels left until you reach it. {remain_refs} {convert_ref}</b>"
        max_ref_lvl = f"<b>💚 You have a new referral level, 3! Maximum level!</b>"
        cur_max_lvl = f"💚 You are at maximum level!</b>"
        next_lvl_remain = "💚 The next level is just a few steps away from being invited. <code>{remain_refs} {person_s}</code>.</b>"
        ref_text = """<b>💎 Referral system

🔗 Your link:
{ref_link}

📔 Our referral system will allow you to earn a large sum without investments. You only need to give your link to friends and you will receive for life <code>{ref_percent}%</code> from their replenishments in the bot.


⚙️ Invited you: {reffer}
💵 Total earned <code>{ref_earn}{curr}</code> from referrals
📌 Total you have <code>{ref_count}</code> {convert_ref}
🎲 Referral level: <code>{ref_lvl}</code>
{mss}"""
        yes_reffer = f"<b>❗ You already have a referral!</b>"
        invite_yourself = "<b>❗ You can't invite yourself</b>"
        new_refferal = "<b>💎 You have a new referral! @{user_name} \n" \
                       "⚙️ Now you have <code>{user_ref_count}</code> {convert_ref}!</b>"
        promo_act = "<b>📩 To activate a promo code, write its name</b>\n" \
                    "<b>⚙️ Example: promo2025</b>"
        no_uses_promocode = "<b>❌ You didn't have time to activate the promo code!</b>"
        no_promocode = "<b>❌ Promo code <code>{promocode}</code> does not exist!</b>"
        yes_promocode = "<b>✅ You have successfully activated the promo code and received <code>{discount}{curr}</code>!</b>"
        yes_uses_promocode = "<b>❌ You have already activated this promo code!</b>"
        no_cats = f"<b>❌ Unfortunately there are no categories at the moment. :(</b>"
        available_cats = f"<b>🛒 Currently available categories:</b>"
        current_cat = "<b>🚀 Current category: <code>{name}</code>:</b>"
        no_products = f"❌ Unfortunately there are no products available at the moment. :("
        open_position_text = """
<b>💎 Category: <code>{cat_name}</code>

🛍️ Item: <code>{pos_name}</code>
💰 Price: <code>{price}{cur}</code>
⚙️ Available quantity: <code>{items}</code></b>

{desc}"""
        no_balance_for_buying = "❗ You don't have enough funds to make a purchase. Top up your balance!"
        confirm_buy_products = """
<b>❓ Do you really want to buy the item(s)??</b>

- Item: <code>{position_name}</code>
- Quantity: <code>{count} pcs.</code>
- Amount to purchase: <code>{price}{curr}</code>
"""
        enter_count_items_for_buy = """
<b>❗ Enter the quantity of items to purchase</b>
⚠️ From <code>1</code> to <code>{items}</code>

- Item: <code>{pos_name}</code> - <code>{price}{curr}</code>
- Your balance: <code>{balance}{curr}</code>
"""
        incorrect_data = "<b>❌ The data was entered incorrectly</b>"
        data_was_edit = "<b>❗ The product you wanted to buy is out of stock</b>"
        incorrect_count_items = "<b>❌ Incorrect quantity of goods</b>"
        no_balance_on_account = "<b>❌ Insufficient funds in the account</b>"
        please_await_products = "<b>🔄 Please wait, the goods are being prepared.</b>"
        successful_buying = """
<b>✅ You have successfully purchased the item(s)</b>

- Receipt: <code>{receipt}</code>
- Item: <code>{position_name} | {purchase_count} pcs. | {purchase_price}{curr}</code>
- Purchase date: <code>{date}</code>
"""
        receipt_purchase = """
<b>⭐ Receipt <code>{receipt}</code>:
📌 Item: <code>{pos_name}</code>
💰 Price: <code>{sum}{curr}</code>
🛒 Quantity: <code>{count} pcs.</code>
🎲 Date: <code>{date}</code>
🔗 Content:</b>
        """
        last_10_purchases = "<b>🚀 Last 10 purchases</b>"
        no_have_purchases = "❗ You don't have any purchases yet.!"
        your_items = "<b>🛒 Your items</b>"
        no_contests = "❌ There are no giveaways going on right now!"
        choose_contest = "<b>🎉 Choose one of the giveaways:</b>"
        contest_text = """
<b>🎉 Giveaway #{contest_id}

💰 Amount: <code>{prize}{cur}</code>

🕒 End in <code>{end_time}</code>

🎉 {winners_num} {winners}
👥 {members_num} {members}</b>"""
        conditions = "\n\n<b>❗ Conditions: </b>\n\n"
        conditions_refills = '<b>💳 {num} {refills} - {status}</b>\n'
        conditions_purchases = '<b>🛒 {num} {purchases} - {status}</b>\n'
        conditions_channels = '<b>✨ Subscribe to {num} {channels_text}: \n\n{channels}</b>\n'
        u_win_the_contest = "<b>🎉 Congratulations, you've won the giveaway! \n💰 A prize of {prize}{cur} has been awarded!</b>"
        u_didnt_have_time_to_enter_contest = "You didn't have time to take part! 💥"
        success = "✅ Success"
        u_already_enter_contest = "❌ You are already participating!"
        contest_already_ended = "💥 The giveaway has already ended!"


    class AdminTexts:
        ### Buttons:
        back = "◀ Back"
        main_settings = "🖤 General settings"
        extra_settings = "🎲 Extra settings"
        switchers = "❗ Switchers"
        statistic = "📊 Statistics"
        find = "🔍 Find"
        products_manage = "💎 Manage items"
        mail = "📌 Mail"
        payments_systems = "💰 Payment systems"
        ad_buttons = "💫 AD buttons"
        mail_buttons = "🧩 Buttons in mail"
        contests = "🎉 Giveaways"
        main_settings_values = {
            "faq": "FAQ",
            "support": "Support",
            "ref_percent_1": "Ref. Percentage lvl 1",
            "ref_percent_2": "Ref. Percentage lvl 2",
            "ref_percent_3": "Ref. Percentage lvl 3",
            "currency": "Bot currency",
            "default_lang": "Default language",
            "chat": "Chat",
            "news": "News channel",
        }
        currencies = {
            "rub": "uzsle",
            "usd": "USD Dollar",
            "eur": "Euro",
        }
        switchers_settings = {
            "tech_works": "Maintenance works",
            "buys": "Purchases",
            "refills": "Replenishments",
            "ref": "Referral system",
            "contests": "Giveaways",
            "multi_lang": "Multilingual",
            "notify": "Notify about new users",
            "sub": "Checking subscriptions",
            "keyboard": "Main menu",
            
        }
        create_promocode = "💎 Create a promo code"
        delete_promocode = "🎲 Delete the promo code"
        edit_number_of_refs_for_ref_lvl_2 = "2️⃣ Change referrals count for lvl 2"
        edit_number_of_refs_for_ref_lvl_3 = "3️⃣ Change referrals count for lvl 3"
        add_category = "➕ | Category"
        edit_category = "⚙️ | Category"
        del_all_categories = "🗑️ | ALL Categories"
        add_subcategory = "➕ | Subcategory"
        edit_subcategory = "⚙️ | Subcategory"
        del_all_subcategories = "🗑️ | ALL Subcategories"
        add_position = "➕ | Position"
        edit_position = "⚙️ | Position"
        del_all_positions = "🗑️ | ALL Positions"
        add_items = "➕ | Items"
        del_item = "🗑️ | Items"
        del_all_items = "🗑️ | ALL Items"
        delete = "🗑️ Delete"
        name = "📘 Title"
        move = "🔁 Move"
        select_this_category = "💎 Select this category"
        photo = "📸 Photo"
        text = "📝 Text"
        file_ = "📁 File"
        price = "💰 Price"
        description = "📑 Description"
        position_type_text = "🪙 Position type"
        clear_items = "🗑️ Clear items"
        get_items = "🧾 Get list of items"
        upload_items = "🔰 Upload items"
        create = "➕ Create"
        current_buttons = "📑 Current buttons"
        open_category_button = "🌐 Open category button"
        open_subcategory_button = "🔰 Open subcategory button"
        open_position_button = "🛒 Open position button"
        open_contest_button = "🎉 Open giveaway button"
        link_button = "🔗 Link button"
        mail_buttons_types = {
            "link": link_button,
            "category": open_category_button,
            "subcategory": open_subcategory_button,
            "position": open_position_button,
            "contest": open_contest_button
        }
        stop_upload_items = "❌ Stop upload items"
        profile = "👤 Profile"
        receipt = "🧾 Receipt"
        edit_balance = "💰 Edit balance"
        unban = "⛔ Unban"
        ban = "⛔ Ban"
        send_message = "⭐ Send message"
        add_balance = "➕ Give balance"
        minus_balance = "➖ Remove balance"
        edit_bal = "⚙️ Edit balance"
        get_users_and_their_balances = "Get users and their balance > 0"
        get_users_ids = "Get a list of user IDs"
        winners_count = "✨ Number of winners"
        prize = "💰 Prize"
        conditions = "🚀 Conditions"
        members_count = "💥 Number of members"
        contest_time = "⌚ Giveaway time"
        end_contest_now = "❌ End giveaway now"
        start_contest = "⭐ Start giveaway"
        purchases_count = "🛒 Number of purchases"
        refills_count = "💳 Number of replenishments"
        channels_ids_for_sub = "💎 Channel IDs to Subscribe to | Qty:"
        edit_custom_pay_method_name = "⚙️ Change method name"
        edit_custom_pay_method_text = "📖 Change text when replenishing"
        edit_custom_pay_method_min_amount = "🚀 Change the minimum amount for replenishment"
        edit_custom_pay_method_receipt = "Ask for a receipt before sending for verification | {status}"
        enable = "✅ Turn on"
        disable = "❌ Turn off"
        get_balance = "💰 Show balance"
        show_info = "📌 Show information"
        
        ### Texts:
        new_refill_custom_pay_method_alert = """
<b>🧾 User {username} [<code>{user_id}</code>] has submitted a payment for review:

Amount: <code>{amount}{curr}</code>

✅ - Approve payment
❌ - Decline payment</b>"""
        enter_new_name_for_custom_pay_method = "<b>⚙️ Enter a new name for the custom payment method.\nCurrent: {name}</b>"
        enter_new_min_for_custom_pay_method = "<b>⚙️ Enter a new minimum for the custom payment method.\nCurrent: {min}{curr}</b>"
        enter_new_text_for_custom_pay_method = "<b>⚙️ Enter new text for the custom payment method.\nCurrent: \n</b>{text}"
        payment_info_custom_pay_method = """
<b>{method}</b>

Status: <code>{status}</code>
Minimum amount for replenishment: <code>{min}{curr}</code>
Preview of replenishment:
{preview_refill}"""
        success = "<b>✅ Success!</b>"
        edit_number_of_refs_for_ref_lvl_alert = "<b>❗ Administrator {username} changed the number of referrals for level <code>{lvl}</code> to <code>{count} {convert}</code></b>"
        you_edit_number_of_refs_for_ref_lvl = "<b>✅ You have changed the number of referrals for level <code>{lvl}</code> to <code>{count} {convert}</code></b>"
        this_promo_is_not_exits = "<b>❌ This promo code does not exist! Try again:</b>"
        this_promo_is_already_exists = "<b>❌ A promo code with this name already exists! Enter another name:</b>"
        promo_is_deleted_alert = "<b>❗ Administrator {username} has removed the Promo Code <code>{name}</code></b>"
        promo_is_deleted = "<b>✅ Promo code <code>{name}</code> successfully removed!</b>"
        promo_is_created_alert = "<b>❗ Administrator {username} created Promo Code <code>{name}</code> with number of uses <code>{uses}</code> and discount <code>{discount}{curr}</code></b>"
        promo_is_created = "<b>✅ Promo code <code>{name}</code> with number of uses <code>{uses}</code> and discount <code>{discount}{curr}</code> has been created!</b>"
        value_is_no_number = "<b>❗ Value must be a number! Try again:</b>"
        enter_discount_for_promo = "<b>❗ Enter the discount (Money will be credited after entering the promo code)</b>"
        now_enter_number_of_uses_for_promo = "<b>❗ Now enter the number of times the promo code is used:</b>"
        enter_new_number_of_refs_for_ref_lvl = "<b>❗ Enter new referrals count for {lvl} level:</b>"
        enter_promo_name_for_delete = "<b>❗ Enter the name of the promo code to delete:</b>"
        enter_promo_name_for_create = "<b>❗ Enter the name of the new promo code:</b>"
        choose_action = "<b>❗ Select action:</b>"
        new_user_alert = "<b>💎 New user registered {name} [<code>{user_id}</code>]</b>"
        edit_main_setting = """
<b>Editing <code>{action}</code>
Current value: 
{value}

Enter new value:</b>
    """
        choose_new_currency = "<b>❗ Select a new bot currency: \n\nP.S. When changing the currency, the prices of goods are converted from the current currency to the new one.</b>"
        choose_new_default_language = "<b>❗ Select a new default language:</b>"
        welcome_to_the_admin_panel = "<b>🎉 Welcome to the admin panel:</b>"
        main_settings_text = "<b>⚙️ General bot settings:</b>"
        choose_what_you_want_to_enable_disable = "<b>⚙️ Select what you want to turn off/on \n❌ - Off | ✅ - On.</b>"
        refill_log = """
<b>💰 Your balance has been replenished!
👤 User: {user_mention} [<code>{user_id}</code>]
💵 Amount: <code>{pay_amount}{curr}</code>
🧾 Receipt: <code>{pay_id}</code>
⚙️ Pay method: <code>{way}</code></b>
    """
        products_manage_text = """
<b>⚙️ Select what you want to do:
<blockquote>➕ - Add/Create
⚙️ - Edit 
🗑️ - Delete</blockquote></b>
        """
        add_category_text = "<b>❗ Enter a name for the category:</b>"
        category_is_created_alert = "<b>❗ Administrator {username} created a category with the name <code>{name}</code>!</b>"
        no_categories_available = "❌ No categories available! Please create at least one!"
        select_category = "<b>❗ Select category:</b>"
        category_text = """
<b>💎 Category: <code>{name}</code>
🆔 ID: <code>{cat_id}</code>
❗ Select what you want to change:</b>
        """
        enter_new_name_for_category = "<b>❗ Enter a new name for the category <code>{name}</code></b>"
        category_is_edited_alert = "<b>❗ Administrator {username} changed the category name from <code>{old_name}</code> to <code>{new_name}</code>!</b>"
        confirm_category_delete = "<b>❓ Are you sure you want to delete the category? <code>{name}</code>?</b>"
        category_is_deleted_alert = "<b>❗ Administrator {username} deleted the category named <code>{name}</code>!</b>"
        del_all_categories_text = "<b>❓ Are you sure you want to delete <u>ALL</u> categories?</b>"
        all_categories_are_deleted_alert = "<b>❗ Administrator {username} has deleted <u>ALL</u> categories!</b>"
        enter_name_for_subcategory = "<b>❗ Enter names for the subcategory:</b>"
        name_error = "<b>❌ Maximum name length is <code>64</code> characters! Try again:</b>"
        description_error = "<b>❌ Maximum description length is <code>2000</code> characters! Try again:</b>"
        subcategory_is_created_alert = "<b>❗ Administrator {username} created a subcategory named <code>{name}</code> in the category <code>{cat_name}</code>!</b>"
        no_subcategories_available = "❌ No subcategories available! Please create at least one!"
        no_subcategories_available_in_this_category = "❌ There are no subcategories available in this category! Please create at least one!"
        no_positions_available_in_this_category = "❌ There are no available positions in this category! Create at least one!"
        no_positions_available = "❌ No positions available! Please create at least one!"
        no_positions_available_in_this_subcategory = "❌ There are no available positions in this subcategory! Create at least one!"
        select_subcategory = "<b>❗ Select subcategory:</b>"
        subcategory_text = """
<b>💎 Subcategory: <code>{name}</code>
🆔 ID: <code>{sub_cat_id}</code>
🎲 Category: <code>{cat_name}</code> [<code>{cat_id}</code>]
❗ Select what you want to change:</b>
        """
        enter_new_name_for_subcategory = "<b>❗ Enter a new name for the subcategory <code>{name}</code></b>"
        subcategory_is_edited_alert = "<b>❗ Administrator {username} changed the subcategory name from <code>{old_name}</code> to <code>{new_name}</code>!</b>"
        confirm_subcategory_delete = "<b>❓ Are you sure you want to delete the subcategory <code>{name}</code>?</b>"
        subcategory_is_deleted_alert = "<b>❗ Administrator {username} deleted the subcategory named <code>{name}</code>!</b>"
        del_all_subcategories_text = "<b>❓ Are you sure you want to delete <u>ALL</u> subcategories?</b>"
        all_subcategories_are_deleted_alert = "<b>❗ Administrator {username} has deleted <u>ALL</u> subcategories!</b>"
        subcategory_has_been_moved_deleted_alert = "<b>❗ Administrator {username} moved subcategory <code>{sub_name}</code> from category <code>{old_cat_name}</code> to category <code>{new_cat_name}</code>!</b>"
        enter_position_name = "<b>❗ Enter a title for the position:</b>"
        enter_position_price = "<b>❗ Enter the price for the item:</b>"
        enter_position_item_type = "<b>❗ Select the item type \n\n<u>⚠️Note:</u> After this step, it is impossible to change the item type!</b>"
        enter_position_description = "<b>❗ Enter a description for the position \nTo avoid placing, send <code>-</code></b>"
        enter_position_photo = "<b>❗ Send a photo for the position \nTo avoid placing, send <code>-</code></b>"
        enter_position_type = "<b>❗ Send <code>+</code> if you want the product to be infinite \nIf you don't want it, enter <code>-</code></b>"
        position_type = {
            True: "Endless items",
            False: "Limited items",
            "file": "File",
            "text": "Text",
            "photo": "Photo"
        }
        position_is_created_alert = """<b>❗ Administrator {username} created the position:
💎 Category: <code>{cat_name}</code> [<code>{cat_id}</code>]
🎲 Subcategory: {subcategory}
📝 Title: <code>{name}</code>
💰 Price: <code>{price}{curr}</code>
🪙 Type: <code>{position_type}</code>
🔰 Items type: <code>{item_type}</code>
🧾 Description: <code>{description}</code></b>
        """
        select_position = "<b>❗ Select position:</b>"
        position_text = """
<b>🌐 Position: <code>{pos_name}</code>
💎 Categoryt: <code>{cat_name}</code> [<code>{cat_id}</code>]
🎲 Subcategory: {subcategory}
💰 Price: <code>{price}{curr}</code>
🪙 Type: <code>{position_type}</code>
🔰 Items type: <code>{item_type}</code>
🧾 Description: <code>{description}</code>
🛒 Number of items: <code>{items_count} pcs.</code>
❗ Select what you want to change:</b>
        """
        enter_new_position_name = "<b>❗ Enter a new name for the position:</b>"
        enter_new_position_price = "<b>❗ Enter a new price for the item:</b>"
        enter_new_position_description = "<b>❗ Enter a new description for the item \nTo remove, send <code>-</code></b>"
        enter_new_position_photo = "<b>❗ Submit a new photo for the position \nTo remove, submit <code>-</code></b>"
        confirm_position_delete = "<b>❓ Are you sure you want to delete the item <code>{name}</code>?</b>"
        position_is_deleted_alert = "<b>❗ Administrator {username} has deleted the item named <code>{name}</code>!</b>"
        confirm_position_items_delete = "<b>❓ Are you sure you want to clear <u>ALL</u> items in item {name}?</b>"
        position_items_is_deleted_alert = "<b>❗ Administrator {username} has deleted <u>ALL</u> items in this item <code>{name}</code>!</b>"
        del_all_positions_text = "<b>❓ Are you sure you want to delete <u>ALL</u> items?</b>"
        all_positions_are_deleted_alert = "<b>❗ Administrator {username} has deleted <u>ALL</u> items!</b>"
        del_all_items_text = "<b>❓ Are you sure you want to delete <u>ALL</u> products?</b>"
        all_items_are_deleted_alert = "<b>❗ Administrator {username} has deleted <u>ALL</u> products!</b>"
        enter_name_for_create_ad_button = "<b>❗ Enter a name for the ad button:</b>"
        enter_content_for_ad_button = "<b>❗ Enter the content (message) of the button:</b>"
        enter_photo_for_ad_button = "<b>❗ Send a photo of the button to skip enter <code>-</code></b>"
        enter_links_buttons_for_ad_button = """<b>❗ Please submit the button links for this button in the format:
    
<code>Link #1|https://examle1.com
Link #2|https://example2.com</code>

❗ To skip enter <code>-</code></b>"""
        ad_button_is_created_alert = "<b>❗ Administrator {username} created an advertising button <code>{name}</code>!</b>"
        ad_button_is_deleted_alert = "<b>❗ Administrator {username} removed the ad button <code>{name}</code>!</b>"
        enter_name_for_delete_ad_button = "<b>❗ Enter the name of the ad button to remove:</b>"
        enter_name_for_create_mail_button = "<b>❗ Enter a name for the button in the newsletter:</b>"
        select_button = "<b>❗ Select button:</b>"
        no_mail_buttons_available = "❗ No buttons available! Please create at least one!"
        select_mail_button_type = "<b>❗ Select button type:</b>"
        enter_link_for_mail_button = "<b>❗ Enter a link for the button in the newsletter:</b>"
        select_contest = "<b>❗ Select a giveaway:</b>"
        enter_data_items = {
            "text": """<b>⚙️ Enter item details:
❗ To separate items, leave a blank line between them. Example:
❗ You can send a txt file where the items are also separated from each other.

<code>Item #1...</code>

<code>Item #2...</code>

<code>Item #3...</code></b>""",
            "text_infinity": "<b>⚙️ Enter item details</b>",
            "photo": """<b>⚙️ Send a photo of the item (with a signature if possible)

❗ Upload one by one</b>""",
            "file": """<b>⚙️ Send the item file (with signature possible)

❗ Upload one by one</b>"""
        }
        products_add_wait = "<b>⌛ Please wait, items are being added...</b>"
        no_need_item_type_sent = "<b>❗ Please send the desired item type!</b>"
        products_successful_added = "<b>✅ Items in the quantity of <code>{count}pcs</code> were successfully added</b>"
        stop_upload_items_text = """<b>✅ Loading of items was completed successfully
⚙️ Items loaded: <code>{count} pcs</code></b>"""
        upload_items_error = "<b>❗ Something went wrong while loading items! Try again!</b>"
        list_of_items = "<b>🧾 List of item items <code>{name}</code></b>"
        get_list_of_items_error = "<b>❗ Something went wrong while trying to get the list of products! Try again!</b>"
        position = "Position"
        item = "Item"
        enter_item_id_for_delete = "<b>❗ Enter the product ID to delete:</b>"
        value_is_no_link = "<b>❗ The value must be a reference! Try again:</b>"
        mail_button_text = """<b>✨ Button: <code>{name}</code>
🌐 Value: {data}
❗ Select what you want to change:</b>"""
        enter_new_mail_button_name = "<b>❗ Enter a new name for the button:</b>"
        confirm_mail_button_delete = "<b>❓ Are you sure you want to remove the button <code>{name}</code>?</b>"
        enter_message_for_mail = "<b>❗ Enter or forward a message for distribution:</b>"
        confirm_message_for_mail = "<b>❓ Are you sure you want to launch a mail with this text??</b>"
        mail_started = "<b>✅ Mail launched!</b>"
        mail_started_alert = "<b>❗ Administrator {username} started the mail!</b>"
        success_mail_text = """<b>✅ The mailing was successfully completed:
    
💎 Total users: <code>{all_users_count} people</code>
✅ Sent successfully: <code>{success_users_count} people</code>
❌ Bot blocked: <code>{failed_users_count} people</code></b>"""
        mail_error = "<b>❌ An unexpected error occurred while sending the mailing.!</b>"
        select_what_you_want_to_find = "<b>⚙️ Select what you want to find:</b>"
        enter_user_profile = "<b>❗ Enter the user ID, name or @username</b>"
        enter_receipt = "<b>❗ Enter the receipt</b>"
        no_user_find = "<b>❗ There is no such user! Double check the data!</b>"
        user_profile_found = """
<b>👤 Profile:

💎 User: {username}
🆔 ID: <code>{user_id}</code>

💰 Balance: <code>{balance}{curr}</code>

💵 Total replenished: <code>{total_refill}{curr}</code>
🧾 Number of refills: <code>{count_refills} pcs.</code>

🛒 Number of purchases: <code>{count_purchases} pcs.</code>
💲 Purchases totaling: <code>{total_purchases}{curr}</code>

📌 Registration date: <code>{reg_date}</code>
🌐 Language: <code>{language}</code>

👥 Referrals: <code>{ref_count} people</code>
🔰 Referral level: <code>{ref_lvl}</code>
🚚 Invited by whom: <code>{ref_name}</code>
💸 Earned from referrals: <code>{ref_earn}{curr}</code></b>
    """
        enter_sum_for_add_to_balance = "<b>💸 Enter the amount to add to your balance:</b>"
        enter_sum_for_minus_from_balance = "<b>💸 Enter the amount to be subtracted from the balance:</b>"
        enter_sum_for_edit_balance = "<b>💸 Enter new user balance:</b>"
        enter_sms_for_user = "<b>❗ Enter messages for the user:</b>"
        new_balance_alert = "<b>❗ Administrator {username} changed the user's balance {user}!</b>"
        receipt_refill = """
<b>⭐ Receipt <code>{receipt}</code>:

⚙️ Type: <code>Replenishment</code>
💎 User: {username}
📌 Pay method: <code>{way}</code>
💰 Amount: <code>{sum}{curr}</code>
🎲 Date: <code>{date}</code>
🔗 Payment link: {url}</b>
        """
        receipt_purchase = """
<b>⭐ Receipt <code>{receipt}</code>:

⚙️ Type: <code>Purchase</code>
💎 User: {username}
📌 Item: <code>{pos_name}</code>
💰 Price: <code>{sum}{curr}</code>
🛒 Quantity: <code>{count} pcs.</code>
🎲 Date: <code>{date}</code>
🔗 Content:</b>
        """
        new_purchase_alert = """
💰 New purchase!
👤 User: <b>{user_name}</b> [<code>{user_id}</code>]
💵 Price: <code>{amount}{curr}</code>
🧾 Receipt: <code>{receipt}</code>
⚙️ Item: <code>{pos_name} x{count}</code>"""
        no_receipt = "❗ Receipt not found, please try again:"
        select_payment = "<b>💰 Select payment system:</b>"
        payments_on_off = {
            True: "✅ On",
            False: "❌ Off",
        }
        payment_info = """
<b>{method}</b>

Status: <code>{status}</code>"""
        balance_info = """
Payment system:
<b>{method}</b>

Balance:
{balance}"""
        get_balance_error = "⚠️ Error while getting balance! Maybe you didn't insert data for payment system!"
        payment_information_text = """
<b>{method}

💰 Replenishments:

Per day: <code>{refills_count_for_day} pcs.</code> (<code>{refills_for_day}{curr}</code>)
Per week: <code>{refills_count_for_week} pcs.</code> (<code>{refills_for_week}{curr}</code>)
Per month: <code>{refills_count_for_month} pcs.</code> (<code>{refills_for_month}{curr}</code>)
For all time: <code>{refills_count_for_all_time} pcs.</code> (<code>{refills_for_all_time}{curr}</code>)

⚙ Information: 

{configs}
⭐ Select what you want to change:</b>
        """
        enter_new_value_for = "<b>❗ Enter a new value for {field}:</b>"
        stats_message = """
<b>📊 Statistics:</b>


<b>👤 Users:</b>

👤 Per day: <code>{users_day}</code>
👤 Per week: <code>{users_week}</code>
👤 Per month: <code>{users_month}</code>
👤 For all time: <code>{users_all}</code>

👤 Sum of balances of all users: <code>{users_money}{cur}</code>

<b>💸 Sales:</b>

💸 Per day: <code>{profit_count_day} pcs.</code> (<code>{profit_amount_day}{cur}</code>)
💸 Per week: <code>{profit_count_week} pcs.</code> (<code>{profit_amount_week}{cur}</code>)
💸 Per month: <code>{profit_count_month} pcs.</code> (<code>{profit_amount_month}{cur}</code>)
💸 For all time: <code>{profit_count_all} pcs.</code> (<code>{profit_amount_all}{cur}</code>)

<b>💰 Replenishments:</b>

💰 Per day: <code>{refill_count_day} pcs.</code> (<code>{refill_amount_day}{cur}</code>)
💰 Per week: <code>{refill_count_week} pcs.</code> (<code>{refill_amount_week}{cur}</code>)
💰 Per month: <code>{refill_count_month} pcs.</code> (<code>{refill_amount_month}{cur}</code>)
💰 For all time: <code>{refill_count_all} pcs.</code> (<code>{refill_amount_all}{cur}</code>)

<b>⚙️ Admins: </b>

⚙️ Total admins: <code>{admins} people</code>
⚙️ Admins: \n"""
        users_balances_txt_text = """Amount: {uzs}₽ | {usd}$ | {eur}€

All users and their balances are greater than 0:

{users_balances}
        """
        all_users_and_their_balances="<b>⚙️All users and their balances</b>"
        list_of_all_users_ids = "<b>⚙️ List of all user IDs</b>"
        sum_is_zero_and_no_users_with_balance = "❗ The sum of balances is 0, there are no users with a balance greater than 0!"
        contest_is_start_successful = "🎉 The giveaway has been successfully launched!"
        edit_contest_settings = """
<b>Editing <code>{action}</code>
Current value: 
{value}

Enter new value:</b>
    """
        contests_settings_values = {
            "winners_num": "Number of winners",
            "prize": "Prize",
            "members_num": "Number of members",
            "end_time": "Giveaway time",
            "purchases_num": "Number of purchases",
            "refills_num": "Number of replenishments",
            "channels_ids": "Channel IDs to subscribe to"
        }
        enter_channels_ids = "<b>❗ Enter the channel IDs to subscribe to, separated by commas. \nExample: -12345678910, -12423562345 \n\nEnter <code>-</code> If you don't want to set. \n\nCurrent value: {value}</b>"
        user_is_entered_contest_alert = "<b>❗ User {user} [<code>{user_id}</code>] is participating in the giveaway on <code>{prize}{cur}</code></b>"
        contest_is_finished_and_members_are_zero_alert = "❗ There were no winners in the {prize}{cur} giveaway, as there were 0 participants!"
        contest_is_finished_alert = "❗ The winners of the {prize}{cur} giveaway were:\n"
        prize_given = "\n\n❗ The prize has been awarded! ❗"