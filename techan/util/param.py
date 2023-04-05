class Parameter:
    candle_stick_pattern = dict(
        bullish=dict(
            hammer=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=-0.00,  # to be valid trend must be less than this value [-1, 0]
                cs_body_position=0.25,  # to be valid body must have a position greater than this value [0, 1]
                body_ls_ratio=1.75,  # to be valid lower shadow must be greater than this value compared to the body [0, inf]
                body_us_ratio=0.50,  # to be valid upper shadow must be less than this value compared to the body [0, inf]
            ),
            piercing=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=-0.00,  # to be valid trend must be less than this value [-1, 0]
            ),
            bullish_engulfing=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=-0.00,  # to be valid trend must be less than this value [-1, 0]
            ),
            morning_star=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=-0.00,  # to be valid trend must be less than this value [-1, 0]
                cs_body_ratio=0.50,  # to be valid body must be greater than this value compared to the cs [0, 1]
                cs_m1_body_ratio=0.50,  # to be valid body must be less than this value compared to the cs [0, 1]
                cs_m2_body_ratio=0.50,  # to be valid body must be greater than this value compared to the cs [0, 1]
                cs_relative_size=0.30,  # to be valid relative size must be greater than this value [0, 1]
                cs_m2_relative_size=0.30,  # to be valid relative size must be greater than this value [0, 1]
            ),
            three_white_soldiers=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=-0.00,  # to be valid trend must be less than this value [-1, 0]
                cs_relative_size=0.25,  # to be valid relative size must be greater than this value [0, 1]
                cs_m1_relative_size=0.25,  # to be valid relative size must be greater than this value [0, 1]
                cs_m2_relative_size=0.25,  # to be valid relative size must be greater than this value [0, 1]
                cs_body_ratio=0.30,  # to be valid body must be greater than this value compared to the cs [0, 1]
                cs_m1_body_ratio=0.30,  # to be valid body must be greater than this value compared to the cs [0, 1]
                cs_m2_body_ratio=0.30,  # to be valid body must be greater than this value compared to the cs [0, 1]
            ),
            bullish_marubozu=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=-0.00,  # to be valid trend must be less than this value [-1, 0]
                cs_relative_size=0.80,  # to be valid relative size must be greater than this value [0, 1]
                cs_body_ratio=0.80,  # to be valid body must be greater than this value compared to the cs [0, 1]
            ),
            three_inside_up=dict(
                trend_window=10,
                trend_strength=-0.00,
                cs_m2_body_ratio=0.50,
                cs_body_ratio=0.50,
                cs_m2_relative_size=0.30,
                cs_relative_size=0.30,
            ),
            bullish_harami=dict(
                trend_window=10,
                trend_strength=-0.00,
                cs_m1_body_ratio=0.50,
                cs_body_ratio=0.50,
                cs_m1_relative_size=0.30,
                cs_relative_size=0.70,
            ),
            tweezer_bottom=dict(
                trend_window=10,
                trend_strength=-0.00,
                cs_m1_body_ratio=0.50,
                cs_body_ratio=0.50,
                cs_m1_relative_size=0.30,
                cs_body_position=-0.25,
            )
        ),
        bearish=dict(
            hanging_man=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=0.00,  # to be valid trend must be greater than this value [0, 1]
                cs_body_position=-0.25,  # to be valid body must have a position less than this value [-1, 0]
                body_ls_ratio=0.50,  # to be valid lower shadow must be less than this value compared to the body [0, inf]
                body_us_ratio=1.50,  # to be valid upper shadow must be greater than this value compared to the body [0, inf]
            ),
            dark_cloud=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=0.00,  # to be valid trend must be greater than this value [0, 1]
            ),
            bearish_engulfing=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=0.00,  # to be valid trend must be greater than this value [0, 1]
            ),
            evening_star=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=0.00,  # to be valid trend must be greater than this value [0, 1]
                cs_body_ratio=0.50,  # to be valid body must be greater than this value compared to the cs [0, 1]
                cs_m1_body_ratio=0.50,  # to be valid body must be less than this value compared to the cs [0, 1]
                cs_m2_body_ratio=0.50,  # to be valid body must be greater than this value compared to the cs [0, 1]
                cs_relative_size=0.30,  # to be valid relative size must be greater than this value [0, 1]
                cs_m2_relative_size=0.30,  # to be valid relative size must be greater than this value [0, 1]
            ),
            three_black_crows=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=-0.00,  # to be valid trend must be less than this value [-1, 0]
                cs_relative_size=0.25,  # to be valid relative size must be greater than this value [0, 1]
                cs_m1_relative_size=0.25,  # to be valid relative size must be greater than this value [0, 1]
                cs_m2_relative_size=0.25,  # to be valid relative size must be greater than this value [0, 1]
                cs_body_ratio=0.30,  # to be valid body must be greater than this value compared to the cs [0, 1]
                cs_m1_body_ratio=0.30,  # to be valid body must be greater than this value compared to the cs [0, 1]
                cs_m2_body_ratio=0.30,  # to be valid body must be greater than this value compared to the cs [0, 1]
            ),
            bearish_marubozu=dict(
                trend_window=10,  # len of trend window [1, inf]
                trend_strength=0.00,  # to be valid trend must be greater than this value [0, 1]
                cs_relative_size=0.80,  # to be valid relative size must be greater than this value [0, 1]
                cs_body_ratio=0.80,  # to be valid body must be greater than this value compared to the cs [0, 1]
            ),
            three_inside_down=dict(
                trend_window=10,
                trend_strength=0.00,
                cs_m2_body_ratio=0.50,
                cs_body_ratio=0.50,
                cs_m2_relative_size=0.30,
                cs_relative_size=0.30,
            ),
            bearish_harami=dict(
                trend_window=10,
                trend_strength=0.00,
                cs_m1_body_ratio=0.50,
                cs_body_ratio=0.50,
                cs_m1_relative_size=0.30,
                cs_relative_size=0.70,
            ),
            tweezer_top=dict(
                trend_window=10,
                trend_strength=0.00,
                cs_m1_body_ratio=0.50,
                cs_body_ratio=0.50,
                cs_m1_relative_size=0.30,
                cs_body_position=0.25,
            )
        ),
    )

