report_types = {
    'channel_basic_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code'],
        'metrics': ['views', 'comments', 'likes', 'dislikes', 'videos_added_to_playlists',
                    'videos_removed_from_playlists', 'shares', 'watch_time_minutes', 'average_view_duration_seconds',
                    'average_view_duration_percentage', 'annotation_click_through_rate', 'annotation_close_rate',
                    'annotation_impressions', 'annotation_clickable_impressions', 'annotation_closable_impressions',
                    'annotation_clicks', 'annotation_closes', 'card_click_rate', 'card_teaser_click_rate',
                    'card_impressions', 'card_teaser_impressions', 'card_clicks', 'card_teaser_clicks',
                    'subscribers_gained', 'subscribers_lost', 'red_views', 'red_watch_time_minutes']
    },
    'channel_cards_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'card_type',
                       'card_id'],
        'metrics': ['card_click_rate', 'card_teaser_click_rate', 'card_impressions', 'card_teaser_impressions',
                    'card_clicks', 'card_teaser_clicks']
    },
    'channel_combined_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'playback_location_type', 'traffic_source_type', 'device_type', 'operating_system'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'channel_demographics_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'age_group', 'gender'],
        'metrics': ['views_percentage']
    },
    'channel_device_os_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'device_type', 'operating_system'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'channel_end_screens_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'end_screen_element_type', 'end_screen_element_id'],
        'metrics': ['end_screen_element_clicks', 'end_screen_element_impressions', 'end_screen_element_click_rate']
    },
    'channel_playback_location_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'playback_location_type', 'playback_location_detail'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'channel_province_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'province_code'],
        'metrics': ['	views', 'watch_time_minutes', 'average_view_duration_seconds',
                    'average_view_duration_percentage', 'annotation_click_through_rate', 'annotation_close_rate',
                    'annotation_impressions', 'annotation_clickable_impressions', 'annotation_closable_impressions',
                    'annotation_clicks', 'annotation_closes', 'card_click_rate', 'card_teaser_click_rate',
                    'card_impressions', 'card_teaser_impressions', 'card_clicks', 'card_teaser_clicks', 'red_views',
                    'red_watch_time_minutes']
    },
    'channel_sharing_service_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'sharing_service'],
        'metrics': ['shares']
    },
    'channel_subtitles_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'subtitle_language', 'subtitle_language_autotranslated'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'channel_traffic_source_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'traffic_source_type', 'traffic_source_detail'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'playlist_basic_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code'],
        'metrics': ['	views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'playlist_combined_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'playback_location_type', 'traffic_source_type', 'device_type',
                       'operating_system'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'playlist_device_os_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'device_type', 'operating_system'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'playlist_playback_location_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'playback_location_type', 'playback_location_detail'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'playlist_province_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'province_code'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'playlist_traffic_source_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'traffic_source_type', 'traffic_source_detail'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    }
}
