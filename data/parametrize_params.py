class AuthParams:

    ddt_redirect_button = {
        'argnames': 'redirect_button',
        'argvalues': [
            'login',
            'register'
        ],
    }

    ddt_registration_auth_methods = {
        'argnames': 'reg_auth_method',
        'argvalues': [
            'phone',
            'email'
        ],
    }

    ddt_redirect_methods = {
        'argnames': 'redirect_method',
        'argvalues': [
            'homepage',
            'reg_form'
        ],
    }

    ddt_prize_number = {
        'argnames': 'prize_number',
        'argvalues': [
            '0',
            '1',
            '2'
        ],
        'ids': ['first_prize', 'second_prize', 'third_price']
    }

    ddt_redirect_to_form = {
        'argnames': 'redirect_to_form',
        'argvalues': [
            'login_form',
            'reg_form'
        ],
    }

    ddt_redirect_link_number = {
        'argnames': 'redirect_link',
        'argvalues': [
            0,
            1,
            2,
            3,
            4,
        ],
        'ids': ['first_link', 'second_link', 'third_link', 'fourth_link', 'fifth_link']
    }
