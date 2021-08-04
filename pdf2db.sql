-- name: get-dc19pdf-list
-- Get list of all pdfs that can be processed
select file_id, foiarchive_file from covid19.files
where ready;

-- name: insert-email!
-- Insert into email
insert into covid19.emails (file_id, file_pg_start, pg_cnt,
    header_begin_ln, header_end_ln, from_email, to_emails, cc_emails,
    subject, attachments, importance, body)
values (:file_id, :file_pg_start, :pg_cnt,
    :header_begin_ln, :header_end_ln, :from_email, :to_emails, :cc_emails,
    :subject, :attachments, :importance, :body);
