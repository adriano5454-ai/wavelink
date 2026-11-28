# Wavelink container with the UI162 release chain.
# Company data remains on the existing persistent disk; no reset is performed.
FROM python:3.13-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends nginx ca-certificates libjpeg62-turbo zlib1g tk8.6 poppler-utils tesseract-ocr tesseract-ocr-por \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 wavelink \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin wavelink
WORKDIR /opt/wavelink
COPY requirements.lock ./requirements.lock
RUN python -m pip install --no-cache-dir -r requirements.lock
COPY vendor/source.part* vendor/source_parts.json ./vendor/
COPY deploy/extract_source.py deploy/apply_ui93.py deploy/apply_ui94.py deploy/apply_ui95.py deploy/apply_ui96.py deploy/apply_ui97.py deploy/apply_ui99.py deploy/apply_ui100.py deploy/apply_ui101.py deploy/apply_ui102.py deploy/apply_ui103.py deploy/apply_ui104.py deploy/apply_ui105.py deploy/apply_ui106.py deploy/apply_ui107.py deploy/apply_ui108.py deploy/apply_ui109.py deploy/apply_ui110.py deploy/apply_ui111.py deploy/apply_ui112.py deploy/apply_ui113.py deploy/apply_ui114.py deploy/apply_ui115.py deploy/apply_ui116.py deploy/apply_ui117.py deploy/apply_ui118.py deploy/apply_ui119.py deploy/apply_ui120.py deploy/apply_ui121.py deploy/apply_ui122.py deploy/apply_ui123.py deploy/apply_ui124.py deploy/apply_ui125.py deploy/apply_ui126.py deploy/apply_ui127.py deploy/apply_ui128.py deploy/apply_ui129.py deploy/apply_ui130.py deploy/apply_ui131.py deploy/apply_ui132.py deploy/apply_ui133.py deploy/apply_ui134.py deploy/apply_ui135.py deploy/apply_ui136.py deploy/apply_ui137.py deploy/apply_ui138.py deploy/apply_ui139.py deploy/apply_ui140.py deploy/apply_ui141.py deploy/apply_ui142.py deploy/apply_ui143.py deploy/apply_ui144.py deploy/apply_ui145.py deploy/apply_ui146.py deploy/apply_ui147.py deploy/apply_ui148.py deploy/apply_ui149.py deploy/apply_ui150.py deploy/apply_ui151.py deploy/apply_ui152.py deploy/apply_ui153.py deploy/apply_ui154.py deploy/apply_ui155.py deploy/apply_ui156.py deploy/apply_ui157.py deploy/apply_ui158.py deploy/apply_ui159.py deploy/apply_ui160.py deploy/apply_ui161.py deploy/apply_ui162.py ./
RUN python extract_source.py vendor/source_parts.json /opt/wavelink/app \
    && python apply_ui93.py /opt/wavelink/app \
    && python apply_ui94.py /opt/wavelink/app \
    && python apply_ui95.py /opt/wavelink/app \
    && python apply_ui96.py /opt/wavelink/app \
    && python apply_ui97.py /opt/wavelink/app \
    && python apply_ui99.py /opt/wavelink/app \
    && python apply_ui100.py /opt/wavelink/app \
    && python apply_ui101.py /opt/wavelink/app \
    && python apply_ui102.py /opt/wavelink/app \
    && python apply_ui103.py /opt/wavelink/app \
    && python apply_ui104.py /opt/wavelink/app \
    && python apply_ui105.py /opt/wavelink/app \
    && python apply_ui106.py /opt/wavelink/app \
    && python apply_ui107.py /opt/wavelink/app \
    && python apply_ui108.py /opt/wavelink/app \
    && python apply_ui109.py /opt/wavelink/app \
    && python apply_ui110.py /opt/wavelink/app \
    && python apply_ui111.py /opt/wavelink/app \
    && python apply_ui112.py /opt/wavelink/app \
    && python apply_ui113.py /opt/wavelink/app \
    && python apply_ui114.py /opt/wavelink/app \
    && python apply_ui115.py /opt/wavelink/app \
    && python apply_ui116.py /opt/wavelink/app \
    && python apply_ui117.py /opt/wavelink/app \
    && python apply_ui118.py /opt/wavelink/app \
    && python apply_ui119.py /opt/wavelink/app \
    && python apply_ui120.py /opt/wavelink/app \
    && python apply_ui121.py /opt/wavelink/app \
    && python apply_ui122.py /opt/wavelink/app \
    && python apply_ui123.py /opt/wavelink/app \
    && python apply_ui124.py /opt/wavelink/app \
    && python apply_ui125.py /opt/wavelink/app \
    && python apply_ui126.py /opt/wavelink/app \
    && python apply_ui127.py /opt/wavelink/app \
    && python apply_ui128.py /opt/wavelink/app \
    && python apply_ui129.py /opt/wavelink/app \
    && python apply_ui130.py /opt/wavelink/app \
    && python apply_ui131.py /opt/wavelink/app \
    && python apply_ui132.py /opt/wavelink/app \
    && python apply_ui133.py /opt/wavelink/app \
    && python apply_ui134.py /opt/wavelink/app \
    && python apply_ui135.py /opt/wavelink/app \
    && python apply_ui136.py /opt/wavelink/app \
    && python apply_ui137.py /opt/wavelink/app \
    && python apply_ui138.py /opt/wavelink/app \
    && python apply_ui139.py /opt/wavelink/app \
    && python apply_ui140.py /opt/wavelink/app \
    && python apply_ui141.py /opt/wavelink/app \
    && python apply_ui142.py /opt/wavelink/app \
    && python apply_ui143.py /opt/wavelink/app \
    && python apply_ui144.py /opt/wavelink/app \
    && python apply_ui145.py /opt/wavelink/app \
    && python apply_ui146.py /opt/wavelink/app \
    && python apply_ui147.py /opt/wavelink/app \
    && python apply_ui148.py /opt/wavelink/app \
    && python apply_ui149.py /opt/wavelink/app \
    && python apply_ui150.py /opt/wavelink/app \
    && python apply_ui151.py /opt/wavelink/app \
    && python apply_ui152.py /opt/wavelink/app \
    && python apply_ui153.py /opt/wavelink/app \
    && python apply_ui154.py /opt/wavelink/app \
    && python apply_ui155.py /opt/wavelink/app \
    && python apply_ui156.py /opt/wavelink/app \
    && python apply_ui157.py /opt/wavelink/app \
    && python apply_ui158.py /opt/wavelink/app \
    && python apply_ui159.py /opt/wavelink/app \
    && python apply_ui160.py /opt/wavelink/app \
    && python apply_ui161.py /opt/wavelink/app \
    && python apply_ui162.py /opt/wavelink/app \
    && rm vendor/source.part* vendor/source_parts.json extract_source.py apply_ui93.py apply_ui94.py apply_ui95.py apply_ui96.py apply_ui97.py apply_ui99.py apply_ui100.py apply_ui101.py apply_ui102.py apply_ui103.py apply_ui104.py apply_ui105.py apply_ui106.py apply_ui107.py apply_ui108.py apply_ui109.py apply_ui110.py apply_ui111.py apply_ui112.py apply_ui113.py apply_ui114.py apply_ui115.py apply_ui116.py apply_ui117.py apply_ui118.py apply_ui119.py apply_ui120.py apply_ui121.py apply_ui122.py apply_ui123.py apply_ui124.py apply_ui125.py apply_ui126.py apply_ui127.py apply_ui128.py apply_ui129.py apply_ui130.py apply_ui131.py apply_ui132.py apply_ui133.py apply_ui134.py apply_ui135.py apply_ui136.py apply_ui137.py apply_ui138.py apply_ui139.py apply_ui140.py apply_ui141.py apply_ui142.py apply_ui143.py apply_ui144.py apply_ui145.py apply_ui146.py apply_ui147.py apply_ui148.py apply_ui149.py apply_ui150.py apply_ui151.py apply_ui152.py apply_ui153.py apply_ui154.py apply_ui155.py apply_ui156.py apply_ui157.py apply_ui158.py apply_ui159.py apply_ui160.py apply_ui161.py apply_ui162.py
COPY vendor/FICTIONAL_DEMO.ajproject ./vendor/FICTIONAL_DEMO.ajproject
COPY deploy ./deploy
RUN python deploy/apply_demo_navigation.py /opt/wavelink/app
COPY ops ./ops
RUN python deploy/apply_corcovado_home.py /opt/wavelink/app
RUN python deploy/apply_profile_language.py /opt/wavelink/app
RUN python deploy/apply_original_file_browser.py /opt/wavelink/app
RUN python deploy/apply_crew_lists.py /opt/wavelink/app
RUN python deploy/apply_work_locations.py /opt/wavelink/app
RUN python deploy/apply_checklist_panel.py /opt/wavelink/app
RUN python deploy/apply_log_locations.py /opt/wavelink/app
RUN python deploy/apply_handover_preview.py /opt/wavelink/app
RUN python deploy/apply_card_feedback.py /opt/wavelink/app
RUN python deploy/apply_inventory_vessels.py /opt/wavelink/app
RUN python deploy/apply_page_vessels.py /opt/wavelink/app
RUN python deploy/apply_feed_news.py /opt/wavelink/app
RUN python deploy/apply_home_news.py /opt/wavelink/app
RUN python deploy/apply_editor_exit.py /opt/wavelink/app
RUN python deploy/apply_roster_location.py /opt/wavelink/app
RUN python deploy/apply_inventory_area.py /opt/wavelink/app
RUN python deploy/apply_inventory_physical.py /opt/wavelink/app
RUN python deploy/apply_hr_mobile_calendar.py /opt/wavelink/app
RUN python deploy/apply_hr_day_count.py /opt/wavelink/app
RUN python deploy/apply_roster_period.py /opt/wavelink/app
RUN python deploy/apply_fault_filters.py /opt/wavelink/app
RUN python deploy/apply_hse_toolbox_filters.py /opt/wavelink/app
RUN python deploy/apply_handover_navigation.py /opt/wavelink/app
RUN python deploy/apply_handover_draft_empty.py /opt/wavelink/app
RUN python deploy/apply_handover_reader.py /opt/wavelink/app
RUN python deploy/apply_handover_shifts.py /opt/wavelink/app
RUN python deploy/apply_hr_org_chart.py /opt/wavelink/app
RUN python deploy/apply_hr_positions.py /opt/wavelink/app
RUN python deploy/apply_hr_org_tree.py /opt/wavelink/app
RUN python deploy/apply_demo_org_example.py /opt/wavelink/app
RUN python deploy/apply_org_card_actions.py /opt/wavelink/app
RUN python deploy/apply_org_dept_leads.py /opt/wavelink/app
RUN python deploy/apply_org_chart_filters.py /opt/wavelink/app
RUN python deploy/apply_demo_chart_locales.py /opt/wavelink/app
RUN python deploy/apply_chart_avatars.py /opt/wavelink/app
RUN python deploy/apply_chart_viewport.py /opt/wavelink/app
RUN python deploy/apply_employee_context.py /opt/wavelink/app
RUN python deploy/apply_handover_files_return.py /opt/wavelink/app
RUN python deploy/apply_employee_sheet.py /opt/wavelink/app
RUN python deploy/apply_calendar_task_preview.py /opt/wavelink/app
RUN python deploy/apply_toolbox_origin.py /opt/wavelink/app
RUN python deploy/apply_toolbox_talk_preview.py /opt/wavelink/app
RUN python deploy/apply_roster_receiving_context.py /opt/wavelink/app
RUN python deploy/apply_placement_locations.py /opt/wavelink/app
RUN python deploy/apply_guest_checklists.py /opt/wavelink/app
RUN python deploy/apply_workspace_search_return.py /opt/wavelink/app
RUN python deploy/apply_receiving_manifest_return.py /opt/wavelink/app
RUN python deploy/apply_certificate_reset.py /opt/wavelink/app
RUN python deploy/apply_handover_preview_history.py /opt/wavelink/app
RUN python deploy/apply_workspace_query_return.py /opt/wavelink/app
RUN python deploy/apply_group_manifest_return.py /opt/wavelink/app
RUN python deploy/apply_journal_history_return.py /opt/wavelink/app
RUN python deploy/apply_record_navigation.py /opt/wavelink/app
RUN python deploy/apply_date_filter_context.py /opt/wavelink/app
RUN python deploy/apply_inventory_open_feedback.py /opt/wavelink/app
RUN python deploy/apply_demo_inventory_expiry.py /opt/wavelink/app
RUN python deploy/apply_alerts_after_app_ready.py /opt/wavelink/app
RUN python deploy/apply_checklist_boot.py /opt/wavelink/app
RUN python deploy/apply_checklist_preview_sections.py /opt/wavelink/app
RUN python deploy/apply_toolbox_early_back.py /opt/wavelink/app
RUN python deploy/apply_demo_outlines.py /opt/wavelink/app
RUN python deploy/apply_toolbox_retained_row.py /opt/wavelink/app
RUN python deploy/apply_pdf_viewer.py /opt/wavelink/app
RUN python deploy/apply_original_job_filter.py /opt/wavelink/app
RUN python deploy/apply_hr_org_transfer.py /opt/wavelink/app
RUN python deploy/apply_original_job_source.py /opt/wavelink/app
RUN python deploy/apply_company_neutral_edges.py /opt/wavelink/app
RUN python deploy/apply_original_mobile_layout.py /opt/wavelink/app
RUN python deploy/apply_source_pdf_viewer.py /opt/wavelink/app
RUN python deploy/apply_readiness.py /opt/wavelink/app
RUN python deploy/apply_tank_readings.py /opt/wavelink/app
RUN python deploy/apply_fleet_positions.py /opt/wavelink/app
RUN python deploy/apply_operations_views.py /opt/wavelink/app
RUN python deploy/apply_consumption.py /opt/wavelink/app
RUN python deploy/apply_fleet_osm.py /opt/wavelink/app
# Runtime starts with mount ownership setup and immediately drops to UID 10001.
# Never install/open the Windows Admin or run its launcher in the container.
EXPOSE 10000
CMD ["python", "-m", "deploy.entrypoint"]
