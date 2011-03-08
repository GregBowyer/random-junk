MERGE INTO pos_clickrates USING
(
  SELECT
    'BR;US;8B;PageTemplate;1;20;pod2;podtemplate2;list2;2' position,
    102 num_clicks,
    202 num_impressions,
    32 alpha,
    40 beta,
    1269862747503 last_update
  FROM
    DUAL
)
pending ON
(
  pos_clickrates.position = pending.position
)
WHEN MATCHED THEN
  UPDATE
  SET
    pos_clickrates.num_clicks      = pending.num_clicks,
    pos_clickrates.num_impressions = pending.num_impressions,
    pos_clickrates.alpha           = pending.alpha,
    pos_clickrates.beta            = pending.beta,
    pos_clickrates.last_update     = pending.last_update 
WHEN NOT MATCHED THEN
  INSERT
    VALUES
    (
      pending.position,
      pending.num_clicks,
      pending.num_impressions,
      pending.alpha,
      pending.beta,
      pending.last_update
    )
    
    SELECT * FROM pos_clickrates WHERE position = 'BR;US;8B;PageTemplate;1;20;pod2;podtemplate2;list2;2';

 UPDATE pos_clickrates 
  SET
    pos_clickrates.num_clicks      = 100,
    pos_clickrates.num_impressions = 200,
    pos_clickrates.alpha           = 1,
    pos_clickrates.beta            = 2,
    pos_clickrates.last_update     = 56489583
  WHERE position = 'BR;US;8B;PageTemplate;1;20;pod2;podtemplate2;list2;2';
