-- 查看所有软件
SELECT 
    id,
    type as "类型",
    model as "机型",
    vendor as "厂家",
    name as "软件名称",
    version as "软件件号",
    status_allow as "允装",
    status_install as "实装",
    status_release as "发布",
    status_receive as "接收",
    release_date as "发布日期"
FROM software
ORDER BY release_date DESC;

-- 查看最新版本的软件（按类型+机型+厂家+名称分组）
WITH latest_versions AS (
    SELECT 
        type,
        model,
        vendor,
        name,
        MAX(release_date) as max_date
    FROM software
    GROUP BY type, model, vendor, name
)
SELECT 
    s.id,
    s.type as "类型",
    s.model as "机型",
    s.vendor as "厂家",
    s.name as "软件名称",
    s.version as "软件件号",
    s.status_allow as "允装",
    s.status_install as "实装",
    s.status_release as "发布",
    s.status_receive as "接收",
    s.release_date as "发布日期"
FROM software s
JOIN latest_versions lv ON 
    s.type = lv.type AND 
    s.model = lv.model AND 
    s.vendor = lv.vendor AND 
    s.name = lv.name AND 
    s.release_date = lv.max_date
WHERE s.status_allow = 1 OR s.status_install = 1
ORDER BY s.type, s.model, s.vendor, s.name, s.release_date DESC;

-- 查看文件信息
SELECT 
    f.id,
    s.name as "软件名称",
    s.version as "软件件号",
    f.file_path as "文件路径",
    f.coc_path as "COC路径",
    f.upload_time as "上传时间"
FROM file f
JOIN software s ON f.software_id = s.id
ORDER BY f.upload_time DESC;

-- 按状态统计软件数量
SELECT 
    SUM(status_allow) as "允装数量",
    SUM(status_install) as "实装数量",
    SUM(status_release) as "发布数量",
    SUM(status_receive) as "接收数量",
    COUNT(*) as "总数量"
FROM software;

-- 按类型统计软件数量
SELECT 
    type as "类型",
    COUNT(*) as "数量"
FROM software
GROUP BY type
ORDER BY COUNT(*) DESC; 