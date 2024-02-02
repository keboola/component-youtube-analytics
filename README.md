# YouTube Analytics Extractor

This data source component uses the YouTube Reporting API to create and run reports that give you insights into the performance of your YouTube
content. Automate data retrieval from
the [YouTube Analytics](https://developers.google.com/youtube/analytics/) reports.

## Prerequisites

1. Get access to your [YouTube Analytics](https://developers.google.com/youtube/analytics/) account.

## Configuration

1. Log in to your account using the Authorize Account button in the Keboola interface.
2. If applicable, you may check the `Use Content Owner ID` checkbox and specify the `Content Owner ID` parameter.
    - This parameter indicates that the request's authorization credentials identify a YouTube CMS user who is acting on
      behalf of the content owner specified in the parameter value. This parameter is intended for YouTube content
      partners that own and manage multiple YouTube channels. It allows content owners to authenticate once and
      get access to all their video and channel data, without having to provide authentication credentials for each
      individual channel. The CMS account that the user authenticates with must be linked to the specified YouTube
      content owner.
3. Select the desired reports in the configuration. For a full list of supported reports, see
   the [Supported reports](#supported-reports) section.

## Supported reports

The connector allows you to run the following reports. The full list of supported reports is available in
the [YouTube Reporting API documentation](https://developers.google.com/youtube/reporting/v1/reports/).

### Channel reports

- [Video reports](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-reports)
    - [User activity](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-user-activity)
    - [User activity by province](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-province)
    - [Playback locations](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-playback-locations)
    - [Traffic sources](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-traffic-sources)
    - [Device type and operating system](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-device-type-and-operating-system)
    - [Viewer demographics](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-viewer-demographics)
    - [Content sharing by platform](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-content-sharing)
    - [Annotations](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-annotations)
    - [Cards](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-cards)
    - [End screens](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-end-screens)
    - [Subtitles](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-subtitles)
    - [Combined](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-combined)
- [Playlist reports](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-reports)
    - [User activity](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-user-activity)
    - [User activity by province](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-province)
    - [Playback locations](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-playback-locations)
    - [Traffic sources](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-traffic-sources)
    - [Device type and operating system](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-device-type-and-operating-system)
    - [Combined](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-combined)

### Content owner reports

- [Video reports](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-reports)
    - [User activity](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-user-activity)
    - [User activity by province](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-province)
    - [Playback locations](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-playback-locations)
    - [Traffic sources](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-traffic-sources)
    - [Device type and operating system](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-device-type-and-operating-system)
    - [Viewer demographics](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-viewer-demographics)
    - [Content sharing by platform](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-content-sharing)
    - [Annotations](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-annotations)
    - [Cards](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-cards)
    - [End screens](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-end-screens)
    - [Subtitles](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-subtitles)
    - [Combined](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#video-combined)
- [Playlist reports](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-reports)
    - [User activity](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-user-activity)
    - [User activity by province](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-province)
    - [Playback locations](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-playback-locations)
    - [Traffic sources](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-traffic-sources)
    - [Device type and operating system](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-device-type-and-operating-system)
    - [Combined](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#playlist-combined)
- [Ad rate reports](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#ad-rate-reports)
- [Estimated revenue reports](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#estimated-revenue-reports)
    - [Estimated video revenue](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#estimated-revenue-videos)
    - [Estimated asset revenue](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#estimated-revenue-assets)
- [Asset reports](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-reports)
    - [User activity](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-user-activity)
    - [User activity by province](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-province)
    - [Video playback locations](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-playback-locations)
    - [Traffic sources](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-traffic-sources)
    - [Device type and operating system](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-device-type-and-operating-system)
    - [Viewer demographics](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-viewer-demographics)
    - [Content sharing by platform](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-content-sharing)
    - [Annotations](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-annotations)
    - [Cards](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-cards)
    - [End screens](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-end-screens)
    - [Combined](https://developers.google.com/youtube/reporting/v1/reports/channel_reports#asset-combined)

## Functionality Notes

- The component uses the [YouTube Reporting API](https://developers.google.com/youtube/reporting/v1/reports/) to
  create and run reports that measure the results of YouTube advertising campaigns.
- **IMPORTANT:** The reporting service creates standardised reports every 24 hours. There is one job for each report type.
  There may be
  more reports (versions) associated with a job. Each report consists of data for one 24-hour period. The system may
  generate more than one report for each 24-hour period. It makes sense to consider only the latest (report's createTime)
  report associated with specific 24-hour period.
    - During the first execution, if there is no job for the specified report_type yet, the job is created and no data is
      downloaded. **The first report may take up to 24 hours to be available.**


Development
-----------

# Raw JSON Configuration Example

```json
{
  "parameters": {
    "report_types": [
      "channel_cards_a1",
      "channel_annotations_a1",
      "channel_basic_a2"
    ],
    "on_behalf_of_content_owner": true,
    "content_owner_id": "123456789"
  }
}
```

If required, change the local data folder (the `CUSTOM_FOLDER` placeholder) path to
your custom path in the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone this repository, init the workspace, and run the component with the following
command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone git@bitbucket.org:kds_consulting_team/kds-team.ex-youtube-analytics.git youtube_analytics
cd youtube_analytics
docker-compose build
docker-compose run --rm dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the test suite and lint check using this command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose run --rm test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration
===========

For information about deployment and integration with Keboola, please refer to the
[deployment section of our developer
documentation](https://developers.keboola.com/extend/component/deployment/).
