/**
 * Type / table inheritance model in oracle
 * conceptually like table inheritance from *gre (ingres / postgres etc)
 * but using nested tables and types instead
 */

-- The type declaration
CREATE TYPE greg.clickrate AS OBJECT (

  /** TODO: Need to work out how to create types with constraints */
  num_clicks          INTEGER   /*NOT NULL*/,
  num_impressions     INTEGER   /*NOT NULL*/,
  click_metric        NUMBER    /*NOT NULL*/,
  impression_metric   NUMBER    /*NOT NULL*/,
  alpha               NUMBER    /*NOT NULL*/,
  beta                NUMBER    /*NOT NULL*/,
  last_update         NUMBER    /*NOT NULL*/
)

-- Type decalaration binding the true type to a table form
CREATE OR REPLACE TYPE clickrate_fact AS TABLE OF clickrate;

-- The Dimension table (NOTE: strictly not a true table ? does this matter?)
CREATE TABLE oid_dim (
  oid INTEGER NOT NULL,
  oid_clickrate clickrate_fact,
  CONSTRAINT pk_oid_clickrate PRIMARY KEY(oid))
  NESTED TABLE oid_clickrate STORE AS oid_clickrate_fact;

-- Example usage - inserts 
INSERT INTO OID_DIM(OID, OID_CLICKRATE) 
  VALUES(1111, CLICKRATE_FACT(CLICKRATE(1, 2, 3, 4, 5.1, 6.1, 12345)));

-- Example useage - selects
SELECT t1.OID, t2.* FROM OID_DIM t1, TABLE(T1.OID_CLICKRATE) t2

-- TODO: Performance / explain plan testing
-- Test MERGE / upsert methods
-- How do indexes work here (in theory given the seperation of dim to fact very well)
-- How to parition (ditto)
