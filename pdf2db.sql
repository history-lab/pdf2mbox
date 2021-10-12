-- name: get-dc19pdf-list
-- Get list of all pdfs that can be processed
select file_id, foiarchive_file from covid19.files
where ready
order by file_id;

-- name: insert-email!
-- Insert into email
insert into covid19.emails (file_id, file_pg_start, pg_cnt, header_begin_ln,
    header_end_ln, from_email, to_emails, cc_emails, bcc_emails,
    attachments, importance, subject, sent_str, body, header_unprocessed)
values (:file_id, :file_pg_start, :pg_cnt, :header_begin_ln,
    :header_end_ln, :from_email, :to_emails, :cc_emails, :bcc_emails,
    :attachments, :importance, :subject, :sent, :body, :header_unprocessed);

-- name: get-emails-in-file
-- Select all emails from a specific file, identified by id.
select email_id, file_pg_start, pg_cnt, header_begin_ln, header_end_ln,
    from_email, to_emails, cc_emails, bcc_emails, attachments, importance,
    subject, sent, body, header_unprocessed
from covid19.emails
where file_id = :file_id;

-- name: get-fauci-emails-pg-start
-- Select all emails from a specific file, identified by id.
select file_pg_start
from covid19.emails
where file_id = '1000'
order by file_pg_start;

-- name: upsert-file-stats!
-- Upsert file_stats
insert into covid19.file_stats (file_id, pg_cnt, email_cnt, type_desc, error_msg)
values (:file_id, :pg_cnt, :email_cnt, :type_desc, :error_msg)
on conflict (file_id) do update set pg_cnt = excluded.pg_cnt,
                                    email_cnt = excluded.email_cnt,
                                    type_desc = excluded.type_desc,
                                    error_msg = excluded.error_msg,
                                    last_update = now();
