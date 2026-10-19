---
name: gillby-water
description: Plan Florida boating, fishing, paddling, surf and beach outings using Gillby's sourced marine forecasts, tides, coastal places and vessel-aware tools. Use for comparing places or departure windows, checking inlet context, planning with a user's saved boat and trips, or researching active cyclones and recorded hurricane tracks since 2000.
---

# Gillby water planning

Help the user compare their actual options by place, time and activity. Use Gillby's current data rather than recalled forecasts or screenshot readings. Gillby covers supported Florida waters; availability varies by location and upstream source.

## Connect and discover

- Product and discovery index: https://www.gillby.com/llms.txt
- Current tool schemas and interpretation notes: https://www.gillby.com/llms-full.txt
- MCP endpoint (Streamable HTTP): https://www.gillby.com/mcp
- HTTP API and OpenAPI: https://www.gillby.com/developers and https://www.gillby.com/api/v1/openapi.json
- Setup, supported clients and account permissions: https://www.gillby.com/integrations

Use an available Gillby connector or MCP connection. Inspect its current tool schemas; names may have a client-specific prefix. Public marine tools require no API key or sign-in. A skill supplies guidance, not an installed MCP connection. If no connector is available, use the documented public HTTP API when your environment supports network requests, or explain the missing connection and link to setup. Do not claim to have queried data you could not retrieve.

## Work from the user's plan

Identify the place, activity, date/time window and relevant constraints. Ask for missing details only when they change the answer. Resolve ambiguous dates and include an explicit local time zone; do not silently substitute current conditions for a future outing. Confirm vessel dimensions and user-supplied equipment limits before boat-specific routing or activity screening.

Resolve a defined spot with `list_spots`. For current conditions, start with `get_conditions` using the resolved ID and `view: "summary"`. Its bundled result may already contain the tides, hazards and source status needed; avoid duplicate calls unless a detail is missing. The MCP arguments retain their nested objects, for example:

```json
{"query":{"spot":"boca-inlet","view":"summary"}}
```

Equivalent public HTTP starting points:

```text
GET https://www.gillby.com/api/v1/spots
GET https://www.gillby.com/api/v1/conditions?spot=boca-inlet&view=summary
```

For a future comparison, request `get_forecast` for each resolved place and the actual window the user wants. Read the live schema for time and activity parameters. Compare departure and return hours, wind/gusts, waves/period/direction, tide/current, relevant advisories and unavailable sources. Use suitable place tools for ramps, fuel, anchorages, reefs or beaches. Verify access and operating details with the operator when they are material to the plan.

For a vessel route, use the user's confirmed draft, air draft, clearance margin and departure time, or their authorized saved vessel. Keep route warnings, depth/bridge assumptions and data gaps attached. A point-depth reading alone cannot establish route clearance.

## Active hurricanes and historical tracks

For active tropical cyclones use `get_hurricanes` with optional `query.basin` (`all`, `al`, `ep`, `cp`). For historical paths use `get_hurricane_history`: finalized NOAA NHC HURDAT2 records for 2000–2025 across the Atlantic and eastern/central Pacific. These public tools need no account or API key.

Use season and basin to distinguish recurring names, or select an exact ID. Request `includeTrack: true` for every recorded point from first observation to last; summaries otherwise omit the track. Example MCP call:

```json
{"name":"get_hurricane_history","arguments":{"query":{"id":"al122005","includeTrack":true}}}
```

HTTP equivalent: `GET https://www.gillby.com/api/v1/tools/get_hurricane_history?id=al122005&includeTrack=true`. Filter by `startYear`, `endYear`, `basin`, `name`, `id`, `hurricanesOnly` or `landfallOnly`; follow returned `nextOffset` for pagination. Full examples and field meanings: https://github.com/OneWave-AI/gillby/blob/main/HURRICANES.md.

Track points use UTC timestamps, coordinates, sustained wind kt and pressure mb. Wind radii are nautical miles ordered NE, SE, SW, NW. Missing measurements are null; landfall flags can refer to any coastline. Active movement bearings point TOWARD, unlike marine wind directions FROM. Keep stale/unavailable status and advisory times. Historical best tracks are retrospective records, not forecasts or damage estimates. Current-season advisories use the active tool. Do not imply the app plots historical paths: it currently shows storm details and official NHC map links.

## Interpret the evidence

- Preserve source names, observation/model times, freshness and QC/unavailable states. A fresh response can still contain an unusable source. Missing is different from zero, no hazard or no observation.
- Local modeled sea height and official marine-zone forecasts cover different waters and times. Surface the official marine forecast and advisories; a lower local estimate does not override them. Offshore sea height is different from breaking surf height and does not describe an inlet by itself.
- Tide heights from different local MLLW gauges do not establish relative channel depths. High tide is not necessarily slack current. Atmospheric visibility is not underwater visibility.
- Activity scores are planning estimates. Do not reuse a different activity's score when the requested one is missing. Use rider-supplied kite wind limits rather than inventing an equipment range.
- Describe lightning as observed/not detected in its stated window, or unavailable. Wildlife and fishing evidence are dated records, not live animal tracking or catch guarantees. Camera frames may be delayed.
- Screenshots and blog examples are historical. Check the current product pages before claiming native apps, Spotify or marketplace plugins are publicly released.

## Personal account actions

Personal vessel, places, trips and preferences require the user's Gillby OAuth. Request only the access needed for the task, through the client's supported authorization flow. Do not ask for service credentials. Read access does not authorize saving, editing, deleting, sharing location or contacting anyone. Perform changes only within the user's explicit request; report the actual result and stop if authorization or the connection is unavailable.

## Give a useful answer

Lead with the comparison or practical next step, tied to the user's activity and time. Use a compact table when comparing places or hours. Include the decisive readings, their times and sources, advisories, and what could not be verified. Link to the relevant Gillby page or map without inventing URL parameters. Separate measured observations, forecasts and your interpretation. Avoid a universal “safe to go” verdict: this planning information does not replace official charts, local notices, beach flags, closures or on-water judgment, and Gillby is not an emergency/rescue service.

Useful requests include comparing Boca and Hillsboro Inlets for a morning boat run, finding a nearby paddle launch with less exposed water, or reviewing a saved boat's proposed route at two departure times. Honor service rate limits and Retry-After rather than retrying indefinitely.
