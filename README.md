# Network Rail Timetable for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/dalebarrie96/HA-Network-Rail-Timetable.svg)](https://github.com/dalebarrie96/HA-Network-Rail-Timetable/releases)

A Home Assistant custom integration that provides real-time train departure information from Network Rail's Live Departure Boards API.

## Features

- 🚂 Real-time train departure information
- ⏱️ Scheduled and estimated departure times
- 🚉 Platform information
- ⚠️ Delay and cancellation status
- 🔄 Automatic updates every 60 seconds
- 🎨 Easy configuration through the UI

## Prerequisites

Before installing this integration, you'll need:

1. **Network Rail API Access Token**
   - Visit [https://raildata.org.uk/](https://raildata.org.uk/)
   - Create a free account
   - Subscribe to the "Live Departure Boards" API
   - Copy your access token

2. **Station CRS Codes**
   - Find your station's 3-letter CRS code (e.g., VIC for Victoria, PAD for Paddington)
   - You can search for codes at [https://www.nationalrail.co.uk/stations/](https://www.nationalrail.co.uk/stations/)

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/dalebarrie96/HA-Network-Rail-Timetable`
6. Select "Integration" as the category
7. Click "Add"
8. Click "Install" on the Network Rail Timetable card
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from [GitHub](https://github.com/dalebarrie96/HA-Network-Rail-Timetable/releases)
2. Extract the `custom_components/network_rail_timetable` folder
3. Copy it to your `custom_components` directory in your Home Assistant configuration folder
4. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Network Rail Timetable"
4. Enter your configuration:
   - **API Key**: Your Network Rail API access token
   - **Home Station**: 3-letter CRS code for your departure station (e.g., VIC)
   - **Destination Station**: 3-letter CRS code for your arrival station (e.g., BRI)
5. Click **Submit**

## Usage

Once configured, the integration creates a sensor entity:

- `sensor.next_train` - Shows the next scheduled or estimated departure time

### Sensor Attributes

The sensor includes additional attributes with detailed information:

| Attribute | Description |
|-----------|-------------|
| `platform` | Departure platform number |
| `origin` | Train origin station |
| `destination` | Train destination station |
| `status` | Current train status (e.g., "On time", "Delayed") |
| `scheduled` | Scheduled departure time |
| `estimated` | Estimated departure time |
| `delayed` | Whether the train is delayed (true/false) |
| `cancelled` | Whether the train is cancelled (true/false) |

### Example Automation

```yaml
automation:
  - alias: "Train Departure Notification"
    trigger:
      - platform: time_pattern
        minutes: "/5"
    condition:
      - condition: time
        after: "07:00:00"
        before: "09:00:00"
      - condition: state
        entity_id: sensor.next_train
        attribute: delayed
        state: "true"
    action:
      - service: notify.mobile_app
        data:
          title: "Train Delayed"
          message: "Your train to {{ state_attr('sensor.next_train', 'destination') }} is delayed. Estimated departure: {{ states('sensor.next_train') }}"
```

### Example Lovelace Card

```yaml
type: entities
title: Next Train
entities:
  - entity: sensor.next_train
    name: Departure Time
    icon: mdi:train
  - type: attribute
    entity: sensor.next_train
    attribute: platform
    name: Platform
  - type: attribute
    entity: sensor.next_train
    attribute: status
    name: Status
  - type: attribute
    entity: sensor.next_train
    attribute: destination
    name: Destination
```

## Troubleshooting

## Support

If you encounter any issues or have questions:

- [Open an issue on GitHub](https://github.com/dalebarrie96/HA-Network-Rail-Timetable/issues)
- Check existing issues for solutions
- Include your Home Assistant version and error logs when reporting issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is not affiliated with or endorsed by Network Rail. Train data is provided by Network Rail's public API.

## Acknowledgments

- Data provided by [Network Rail](https://www.networkrail.co.uk/)
- API access via [RailData Marketplace](https://raildata.org.uk/)
