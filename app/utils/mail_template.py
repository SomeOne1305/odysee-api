def template_mail(token: str, user_name: str = "User", expiration_minutes: int = 10):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirm Your Email</title>
    <style>
        /* Reset styles for email compatibility */
        body, table, td, a {{
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }}
        table, td {{
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }}
        img {{
            border: 0;
            height: auto;
            line-height: 100%;
            outline: none;
            text-decoration: none;
            -ms-interpolation-mode: bicubic;
        }}
        p {{
            display: block;
            margin: 13px 0;
        }}
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f7f7f7; font-family: Arial, sans-serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
        <!-- Header Section -->
        <tr>
            <td align="center" bgcolor="#ffffff" style="padding: 20px 0; border-bottom: 3px solid #e6598c;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td align="center" style="padding: 20px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/11516/11516677.png" style="width:70px;height:70px;display:block;margin:0 auto;"/>
                            <h2 style="color: #ca004b; font-size: 25px; margin: 15px 0;">Welcome, {user_name}!</h2>
                            <p style="font-size: 16px; color: #333333; line-height: 1.5; text-align: center;">
                                Thanks for signing up! To complete your registration, please confirm your email address by clicking the button below.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <!-- Content Section -->
        <tr>
            <td align="center" bgcolor="#ffffff" style="padding: 20px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td align="center" style="padding: 20px;">
                            <a href="http://localhost:3000/confirm/{token}" target="_blank" style="background-color: #ca004b; color: #ffffff; font-size: 18px; text-decoration: none; padding: 12px 24px; border-radius: 5px; display: inline-block;">
                                Confirm Email
                            </a>
                            <p style="font-size: 14px; color: #666666; margin-top: 15px;">
                                This link will expire in {expiration_minutes} minutes. If you didn't request this, please ignore this email.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <!-- Footer Section -->
        <tr>
            <td align="center" bgcolor="#f7f7f7" style="padding: 20px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td align="center" style="font-size: 14px; color: #666666;">
                            <p>Best regards,</p>
                            <p><strong>Odysee</strong> (Clone Project)</p>
                            <p style="font-size: 12px; color: #999999;">
                                This is a personal project and not affiliated with any official organization.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""