import time
from playwright.sync_api import sync_playwright
B="http://127.0.0.1:28091"; out="/tmp/cbva/evidence"
with sync_playwright() as p:
    br=p.chromium.launch()
    ctx=br.new_context(viewport={"width":1440,"height":900},record_video_dir=out,record_video_size={"width":1440,"height":900})
    pg=ctx.new_page()
    pg.goto(B+"/ui/index.html"); pg.wait_for_selector("#auth-username-input",timeout=60000)
    pg.fill("#auth-username-input","Administrator"); pg.fill("#auth-password-input","password")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(6000)
    def shot(url,name,wait=5000):
        pg.goto(B+url); pg.wait_for_timeout(wait); pg.screenshot(path=f"{out}/{name}.png",full_page=True)
    shot("/ui/index.html#/overview/stats","01-dashboard")
    shot("/ui/index.html#/buckets","02-buckets")
    shot("/ui/index.html#/collections?collectionsBucket=voltagent","03-scopes-collections")
    # expand support_demo scope if collapsed
    try:
        pg.get_by_text("support_demo").first.click(); pg.wait_for_timeout(2500)
    except Exception as e: print("expand", e)
    pg.screenshot(path=f"{out}/03b-support_demo-knowledge.png",full_page=True)
    shot("/ui/index.html#/docs/editor?bucket=voltagent&scope=support_demo&collection=knowledge","04-documents",7000)
    shot("/ui/index.html#/index","05-indexes-overview",6000)
    pg.goto(B+"/ui/index.html#/query/workbench"); pg.wait_for_timeout(7000)
    def run(q,name):
        ed=pg.locator(".ace_text-input").first
        ed.focus(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.keyboard.insert_text(q)
        pg.wait_for_timeout(800); pg.get_by_role("button", name="Execute").click(); pg.wait_for_timeout(7000)
        pg.screenshot(path=f"{out}/{name}.png",full_page=True)
    run("SELECT name, keyspace_id, scope_id, `using`, index_key, `with`, state FROM system:indexes WHERE bucket_id = 'voltagent'","06-hyperscale-index-definition")
    run("SELECT k.id, k.metadata.title, APPROX_VECTOR_DISTANCE(k.`vector`, [1,0,0], 'COSINE') AS distance FROM voltagent.support_demo.knowledge k ORDER BY APPROX_VECTOR_DISTANCE(k.`vector`, [1,0,0], 'COSINE') LIMIT 3","07-hyperscale-vector-query")
    run("EXPLAIN SELECT v.id, APPROX_VECTOR_DISTANCE(v.`vector`, [1,0,0], 'COSINE') AS distance FROM voltagent.support_demo.knowledge AS v WHERE v.documentType = 'support_knowledge_chunk' ORDER BY distance ASC LIMIT 3","08-explain-uses-hyperscale-index")
    pg.get_by_text("Plan Text").first.click(); pg.wait_for_timeout(2000); pg.screenshot(path=f"{out}/09-plan-text-indexscan3.png",full_page=True)
    ctx.close(); br.close()
