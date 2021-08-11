-- name: get-dc19pdf-list
-- Get list of all pdfs that can be processed
select file_id, foiarchive_file from covid19.files
where ready  /* and file_id between 110 and 120 */
order by file_id;

-- name: insert-email!
-- Insert into email
insert into covid19.emails (file_id, file_pg_start, pg_cnt,
    header_begin_ln, header_end_ln, from_email, to_emails, cc_emails,
    subject, attachments, importance, body)
values (:file_id, :file_pg_start, :pg_cnt,
    :header_begin_ln, :header_end_ln, :from_email, :to_emails, :cc_emails,
    :subject, :attachments, :importance, :body);

-- name: upsert-file-stats!
-- Upsert file_stats
insert into covid19.file_stats (file_id, pg_cnt, email_cnt, type_desc, error_msg)
values (:file_id, :pg_cnt, :email_cnt, :type_desc, :error_msg)
on conflict (file_id) do update set pg_cnt = excluded.pg_cnt,
                                    email_cnt = excluded.email_cnt,
                                    type_desc = excluded.type_desc,
                                    error_msg = excluded.error_msg,
                                    last_update = now();
