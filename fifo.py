import streamlit as st

"""
FIFO (First In First Out) Cache Replacement Algorithm
"""

def simulate(requests, cache_size, step_callback):
    cache = []
    hits = 0
    misses = 0
    fifo_queue = []

    for step, request in enumerate(requests):
        replaced_index = None
        hit_index = None

        if request in cache:
            hits += 1
            hit_index = cache.index(request)
        else:
            misses += 1
            if len(cache) < cache_size:
                cache.append(request)
                fifo_queue.append(request)
            else:
                oldest = fifo_queue.pop(0)
                replaced_index = cache.index(oldest)
                cache[replaced_index] = request
                fifo_queue.append(request)

        state = {
            "step": step + 1,
            "request": request,
            "cache": cache.copy(),
            "replaced_index": replaced_index,
            "hit_index": hit_index,
            "queue": fifo_queue.copy()
        }
        step_callback(state)

    return hits, misses


# ================= Streamlit UI =================

st.title("🧠 FIFO Cache Simulation")

requests_input = st.text_input(
    "Page Requests (comma separated)",
    "1,2,3,4,1,2,5,1,2,3,4,5"
)

cache_size = st.selectbox("Cache Size", [3, 4, 5, 8])

if st.button("Run Simulation"):
    requests = [int(x.strip()) for x in requests_input.split(",")]
    steps = []

    def callback(state):
        steps.append(state)

    hits, misses = simulate(requests, cache_size, callback)

    st.subheader("📊 Results")
    st.write(f"✅ Hits: {hits}")
    st.write(f"❌ Misses: {misses}")

    st.subheader("🔍 Step-by-Step")

    for s in steps:
        st.markdown(f"### Step {s['step']} → Request `{s['request']}`")

        if s["hit_index"] is not None:
            st.success(f"HIT at index {s['hit_index']}")
        else:
            st.error("MISS")

        if s["replaced_index"] is not None:
            st.warning(f"Replaced index {s['replaced_index']}")

        st.write("Cache:", s["cache"])
        st.write("FIFO Queue:", s["queue"])
        st.divider()
