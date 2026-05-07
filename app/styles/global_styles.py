def load_global_styles():
    return """
    <style>
        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"] {
            background: #0B0F17;
            color: #F9FAFB;
        }

        [data-testid="stHeader"] {
            background: #0B0F17;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 34px;
            padding-bottom: 36px;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }

        .app-header {
            margin-bottom: 5px;
        }

        .app-title {
            font-size: 28px;
            font-weight: 850;
            color: #F9FAFB;
            line-height: 1.15;
        }

        .app-subtitle {
            font-size: 15px;
            color: #CBD5E1;
            margin-bottom: 14px;
            max-width: 820px;
            line-height: 1.5;
            word-break: normal;
            overflow-wrap: normal;
            hyphens: none;
        }

        .section-title {
            font-size: 15px;
            font-weight: 800;
            color: #F9FAFB;
            margin-top: 0;
            margin-bottom: 6px;
        }

        .section-caption {
            color: #94A3B8;
            font-size: 12px;
            line-height: 1.45;
            margin-bottom: 8px;
        }

        .system-strip {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 8px;
            margin: 0 0 14px 0;
        }

        .system-step {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 7px 9px;
            min-width: 0;
            min-height: 42px;
        }

        .system-step-label {
            color: #F9FAFB;
            font-size: 12px;
            font-weight: 800;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .system-step-owner {
            color: #94A3B8;
            font-size: 10px;
            margin-top: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
            margin-bottom: 6px;
        }

        .status-badge-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 7px;
            margin-bottom: 7px;
        }

        .status-badge {
            background: #0B1220;
            border: 1px solid #243244;
            border-radius: 999px;
            padding: 6px 9px;
            min-width: 0;
        }

        .status-label {
            color: #94A3B8;
            font-size: 9.5px;
            font-weight: 850;
            text-transform: uppercase;
            display: block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .status-value {
            color: #E5E7EB;
            font-size: 10.5px;
            font-weight: 850;
            display: block;
            margin-top: 1px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .orchestration-strip {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 7px;
        }

        .orchestration-chip {
            background: #0B1220;
            border: 1px solid #243244;
            border-radius: 999px;
            color: #CBD5E1;
            font-size: 11px;
            font-weight: 750;
            padding: 5px 9px;
            white-space: nowrap;
        }

        .orchestration-chip strong {
            color: #60A5FA;
        }

        .summary-item {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 7px 9px;
            min-width: 0;
        }

        .summary-label {
            color: #94A3B8;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
        }

        .summary-value {
            color: #F9FAFB;
            font-size: 13px;
            font-weight: 850;
            margin-top: 3px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .summary-value.risk-low {
            color: #4ADE80;
        }

        .summary-value.risk-medium {
            color: #FBBF24;
        }

        .summary-value.risk-high {
            color: #F87171;
        }

        .response-card {
            background: #F1F5F9;
            color: #111827;
            padding: 11px 14px;
            border-radius: 8px;
            border: 1px solid #CBD5E1;
            font-size: 12.5px;
            line-height: 1.34;
            width: 100%;
            max-height: 125px !important;
            overflow-y: auto !important;
        }

        .response-label {
            color: #CBD5E1;
            font-size: 12.5px;
            font-weight: 850;
            text-transform: uppercase;
            margin: 8px 0 5px 0;
            letter-spacing: 0;
        }

        .empty-response {
            background: #111827;
            border: 1px dashed #334155;
            border-radius: 8px;
            color: #94A3B8;
            box-sizing: border-box;
            margin: 0;
            padding: 9px 12px;
            font-size: 12.5px;
            line-height: 1.3;
        }

        .timeline {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 7px;
            margin-top: 10px;
            margin-bottom: 10px;
        }

        .agent-timeline-grid {
            display: grid !important;
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
            gap: 7px !important;
            margin-top: 10px !important;
            margin-bottom: 10px !important;
            padding-bottom: 0 !important;
        }

        .timeline-item {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 7px 9px;
            min-width: 0;
            min-height: 44px;
        }

        .timeline-step {
            color: #F9FAFB;
            font-size: 11px;
            font-weight: 850;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .timeline-detail {
            color: #94A3B8;
            font-size: 10.5px;
            line-height: 1.3;
            margin-top: 2px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .guardrail-list {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
            margin-top: 8px;
        }

        .guardrail-item {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            color: #CBD5E1;
            font-size: 12px;
            line-height: 1.35;
            padding: 9px 10px;
        }

        .guardrail-item strong {
            color: #F9FAFB;
        }

        .detail-section {
            margin-top: 20px;
        }

        .details-shortcut {
            margin-top: 10px;
            padding: 8px 10px;
            border: 1px solid #334155;
            border-radius: 8px;
            background: #0D1524;
            color: #94A3B8;
            font-size: 11.5px;
            line-height: 1.35;
            transition: border-color 120ms ease, background 120ms ease;
        }

        .details-shortcut a {
            display: inline-flex;
            align-items: center;
            color: #60A5FA;
            font-size: 12px;
            font-weight: 850;
            text-decoration: none;
            margin-bottom: 2px;
        }

        .details-shortcut:hover {
            border-color: #3B82F6;
            background: #0F1A2E;
        }

        .details-shortcut a:hover {
            color: #93C5FD;
            text-decoration: none;
        }

        .detail-card {
            background: #0F172A;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 14px 16px;
        }

        .reason-box {
            background: #111827;
            border-left: 3px solid #60A5FA;
            color: #CBD5E1;
            padding: 7px 10px;
            border-radius: 6px;
            font-size: 11px;
            line-height: 1.25;
            margin-bottom: 6px;
        }

        .reason-box strong {
            color: #F9FAFB;
            display: block;
            margin-bottom: 2px;
        }

        .reason-box ul {
            margin: 0;
            padding-left: 16px;
        }

        .reason-box li {
            margin: 0;
        }

        .reason-data-signals {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 6px;
            padding-top: 6px;
            border-top: 1px solid #1E293B;
        }

        .data-signal-row {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
            margin: 0 0 8px 0;
        }

        .data-signal-label {
            color: #94A3B8;
            font-size: 10.5px;
            font-weight: 850;
            text-transform: uppercase;
            margin-right: 2px;
        }

        .data-signal-chip {
            background: #0B1220;
            border: 1px solid #243244;
            border-radius: 999px;
            color: #CBD5E1;
            font-size: 10px;
            font-weight: 750;
            padding: 3px 7px;
            white-space: nowrap;
        }

        .data-signal-strip {
            margin-top: 0;
            margin-bottom: 8px;
        }

        .review-ticket-link {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            background: #0B1220;
            border: 1px solid #2563EB;
            border-radius: 8px;
            color: #DBEAFE;
            font-size: 12px;
            font-weight: 850;
            line-height: 1.3;
            padding: 8px 10px;
            margin-top: 9px;
        }

        .review-ticket-link small {
            color: #94A3B8;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
        }

        .metric-card {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 14px 16px;
            color: #E5E7EB;
        }

        .metric-label {
            color: #94A3B8;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .metric-value {
            color: #F9FAFB;
            font-size: 16px;
            font-weight: 850;
            margin-top: 4px;
        }

        div.stButton > button {
            height: 40px;
            font-size: 15px;
            font-weight: 750;
            border-radius: 8px;
            background: #2563EB;
            border: none;
        }

        div.stButton > button:hover {
            background: #1D4ED8;
            border: none;
        }

        textarea {
            font-size: 13px !important;
            background: #1F2430 !important;
            color: #F9FAFB !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 8px;
            border-color: #243244;
            background: #0F172A;
        }

        div[data-testid="stExpander"] {
            border-color: #243244;
            background: #0F172A;
            border-radius: 8px;
        }

        div[data-baseweb="select"] > div {
            background: #1F2430;
            border-color: #243244;
            color: #F9FAFB;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 14px 16px 18px 16px;
        }

        div[data-testid="stSelectbox"] {
            margin-bottom: 4px;
        }

        @media (max-width: 900px) {
            .system-strip,
            .summary-grid,
            .status-badge-grid,
            .timeline,
            .guardrail-list {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """
