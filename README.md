# todolist-flask
Todolist app using Flask

<details><summary>todolist_flask.mp4</summary>

<video controls src="https://github.com/user-attachments/assets/8b3e39ad-09b7-45fe-b53b-55d0616f4578" muted="false"></video>

</details>

## Setup

```bash
alembic upgrade head
```

## Run

```bash
python src/app.py
```

Open http://localhost:3000/ or https://localhost:3443/

## pytest

```bash
pytest .
```

## Customizing Flask and Vue3 Delimiters

```python
app = Flask(__name__)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
```

```javascript
const app = Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
```
