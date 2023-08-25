"""
Each output table is associated with a specific report type ID.
Here were prepared a structure listing dimensions a metrics that appear in specific report type ID.
We currently use only 'dimensions' list to specify which columns compose a primary key of the table.
The 'metrics' list are not used. We have it here only for completion.

Information on dimensions and metrics for individual report type IDs was retrieved from documentation found here:
- https://developers.google.com/youtube/reporting/v1/reports/channel_reports
- https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports
"""

report_types = {
    'channel_annotations_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'live_or_on_demand', 'subscribed_status', 'country_code',
                       'annotation_type', 'annotation_id'],
        'metrics': ['annotation_click_through_rate', 'annotation_close_rate', 'annotation_impressions',
                    'annotation_clickable_impressions', 'annotation_closable_impressions', 'annotation_clicks',
                    'annotation_closes']
    },
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
    },
    'content_owner_basic_a3': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code'],
        'metrics': ['views', 'comments', 'shares', 'watch_time_minutes', 'average_view_duration_seconds',
                    'average_view_duration_percentage', 'annotation_click_through_rate', 'annotation_close_rate',
                    'annotation_impressions', 'annotation_clickable_impressions', 'annotation_closable_impressions',
                    'annotation_clicks', 'annotation_closes', 'card_click_rate', 'card_teaser_click_rate',
                    'card_impressions', 'card_teaser_impressions', 'card_clicks', 'card_teaser_clicks',
                    'subscribers_gained', 'subscribers_lost', 'videos_added_to_playlists',
                    'videos_removed_from_playlists', 'likes', 'dislikes', 'red_views', 'red_watch_time_minutes']
    },
    'content_owner_province_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'province_code'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'annotation_click_through_rate', 'annotation_close_rate', 'annotation_impressions',
                    'annotation_clickable_impressions', 'annotation_closable_impressions', 'annotation_clicks',
                    'annotation_closes', 'card_click_rate', 'card_teaser_click_rate', 'card_impressions',
                    'card_teaser_impressions', 'card_clicks', 'card_teaser_clicks', 'red_views',
                    'red_watch_time_minutes']
    },
    'content_owner_playback_location_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'playback_location_type', 'playback_location_detail'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'content_owner_traffic_source_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'traffic_source_type', 'traffic_source_detail'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'content_owner_device_os_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'device_type', 'operating_system'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'content_owner_demographics_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'age_group', 'gender'],
        'metrics': ['']
    },
    'content_owner_sharing_service_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'sharing_service'],
        'metrics': ['shares']
    },
    'content_owner_annotations_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'annotation_type', 'annotation_id'],
        'metrics': ['annotation_click_through_rate', 'annotation_close_rate', 'annotation_impressions',
                    'annotation_clickable_impressions', 'annotation_closable_impressions', 'annotation_clicks',
                    'annotation_closes']
    },
    'content_owner_cards_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'card_type', 'card_id'],
        'metrics': ['card_click_rate', 'card_teaser_click_rate', 'card_impressions', 'card_teaser_impressions',
                    'card_clicks', 'card_teaser_clicks']
    },
    'content_owner_end_screens_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'end_screen_element_type', 'end_screen_element_id'],
        'metrics': ['end_screen_element_clicks', 'end_screen_element_impressions', 'end_screen_element_click_rate']
    },
    'content_owner_subtitles_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'subtitle_language', 'subtitle_language_autotranslated'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'content_owner_combined_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'live_or_on_demand',
                       'subscribed_status', 'country_code', 'playback_location_type', 'traffic_source_type',
                       'device_type', 'operating_system'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'average_view_duration_percentage',
                    'red_views', 'red_watch_time_minutes']
    },
    'content_owner_playlist_basic_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'content_owner_playlist_province_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'province_code'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'content_owner_playlist_playback_location_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'playback_location_type', 'playback_location_detail'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'content_owner_playlist_traffic_source_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'traffic_source_type', 'traffic_source_detail'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'content_owner_playlist_device_os_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'device_type', 'operating_system'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'content_owner_playlist_combined_a1': {
        'dimensions': ['date', 'channel_id', 'playlist_id', 'video_id', 'live_or_on_demand', 'subscribed_status',
                       'country_code', 'playback_location_type', 'traffic_source_type', 'device_type',
                       'operating_system'],
        'metrics': ['views', 'watch_time_minutes', 'average_view_duration_seconds', 'playlist_starts',
                    'playlist_saves_added', 'playlist_saves_removed']
    },
    'content_owner_ad_rates_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'country_code', 'ad_type'],
        'metrics': ['estimated_youtube_ad_revenue', 'ad_impressions', 'estimated_cpm']
    },
    'content_owner_estimated_revenue_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'claimed_status', 'uploader_type', 'country_code'],
        'metrics': ['estimated_partner_revenue', 'estimated_partner_ad_revenue', 'estimated_partner_ad_auction_revenue',
                    'estimated_partner_ad_reserved_revenue', 'estimated_youtube_ad_revenue',
                    'estimated_monetized_playbacks', 'estimated_playback_based_cpm', 'ad_impressions', 'estimated_cpm',
                    'estimated_partner_red_revenue', 'estimated_partner_transaction_revenue']
    },
    'content_owner_asset_estimated_revenue_a1': {
        'dimensions': ['date', 'channel_id', 'video_id', 'asset_id', 'claimed_status', 'uploader_type', 'country_code'],
        'metrics': ['estimated_partner_revenue', 'estimated_partner_ad_revenue', 'estimated_partner_ad_auction_revenue',
                    'estimated_partner_ad_reserved_revenue', 'estimated_partner_red_revenue',
                    'estimated_partner_transaction_revenue']
    },
    'content_owner_asset_basic_a2': {
        'dimensions': ['date', 'channel_id', 'video_id', 'asset_id', 'claimed_status', 'uploader_type',
                       'live_or_on_demand', 'subscribed_status', 'country_code'],
        'metrics': ['views', 'comments', 'likes', 'dislikes', 'videos_added_to_playlists',
                    'videos_removed_from_playlists', 'shares', 'watch_time_minutes', 'average_view_duration_seconds',
                    'average_view_duration_percentage', 'annotation_click_through_rate', 'annotation_close_rate',
                    'annotation_impressions', 'annotation_clickable_impressions', 'annotation_closable_impressions',
                    'annotation_clicks', 'annotation_closes', 'card_click_rate', 'card_teaser_click_rate',
                    'card_impressions', 'card_teaser_impressions', 'card_clicks', 'card_teaser_clicks', 'red_views',
                    'red_watch_time_minutes']
    }
}
