'''
Just a utility file to store some SQL queries for easy reference

@author: Toby Murray
'''
createChangesetTable = '''CREATE EXTENSION IF NOT EXISTS hstore;
  CREATE TABLE osm_changeset (
  id bigint,
  user_id bigint,
  created_at timestamp without time zone,
  min_lat numeric(10,7),
  max_lat numeric(10,7),
  min_lon numeric(10,7),
  max_lon numeric(10,7),
  closed_at timestamp without time zone,
  open boolean,
  num_changes integer,
  user_name varchar(255),
  tags hstore
);
CREATE TABLE osm_changeset_comment (
  comment_changeset_id bigint not null,
  comment_user_id bigint not null,
  comment_user_name varchar(255) not null,
  comment_date timestamp without time zone not null,
  comment_text text not null
);
CREATE TABLE osm_changeset_state (
  last_sequence bigint,
  last_timestamp timestamp without time zone,
  update_in_progress smallint
);
'''
createOsmHistoryTable = '''
CREATE TABLE if not EXISTS public.osm_element_history (
	id int8 NULL,
	"type" varchar NULL,
	tags hstore NULL,
	lat numeric(9, 7) NULL,
	lon numeric(10, 7) NULL,
	nds _int8 NULL,
	members _int8 NULL,
	changeset int8 NULL,
	"timestamp" timestamp NULL,
	uid int8 NULL,
	"version" int8 NULL,
	"action" varchar NULL,
	country varchar NULL,
	CONSTRAINT osm_element_history_un UNIQUE (id, version,"type")
);

CREATE TABLE if not EXISTS public.osm_element_history_state (
	last_sequence int8 NULL,
	last_timestamp timestamp NULL,
	update_in_progress int2 NULL
);

'''

initStateTable = '''INSERT INTO osm_changeset_state VALUES (-1, null, 0)''';

dropIndexes = '''ALTER TABLE osm_changeset DROP CONSTRAINT IF EXISTS osm_changeset_pkey CASCADE;
DROP INDEX IF EXISTS user_name_idx, user_id_idx, created_idx, tags_idx, changeset_geom_gist ;
'''

createConstraints = '''ALTER TABLE osm_changeset ADD CONSTRAINT osm_changeset_pkey PRIMARY KEY(id);'''

createIndexes = '''CREATE INDEX user_name_idx ON osm_changeset(user_name);
CREATE INDEX user_id_idx ON osm_changeset(user_id);
CREATE INDEX created_idx ON osm_changeset(created_at);
CREATE INDEX tags_idx ON osm_changeset USING GIN(tags);
'''

createGeometryColumn = '''
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT AddGeometryColumn('osm_changeset','geom', 4326, 'POLYGON', 2);
'''

createGeomIndex = '''
CREATE INDEX changeset_geom_gist ON osm_changeset USING GIST(geom);
'''

createBoundaries = '''
CREATE TABLE if not exists public.boundaries (
	name_en varchar NULL,
	admin_level int4 NULL,
	tags hstore NULL,
	boundary geometry NULL,
	priority bool NULL
);
CREATE UNIQUE INDEX if not exists boundaries_nameen_idx ON public.boundaries USING btree (name_en);
'''

