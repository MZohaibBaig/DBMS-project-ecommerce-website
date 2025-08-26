import os, subprocess, textwrap, sys

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Wrote", path)

base_html = """{% load static %}
<!doctype html>
<html lang="en" data-bs-theme="auto">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>LensHive</title>

    <!-- Bootstrap 5 -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
      crossorigin="anonymous"
    >
    <!-- Bootstrap Icons -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
      rel="stylesheet"
    >
    <!-- App CSS -->
    <link href="{% static 'shop2/app.css' %}" rel="stylesheet" />

    <meta name="color-scheme" content="light dark">
  </head>
  <body>
    <nav class="navbar navbar-expand-md bg-body-tertiary border-bottom sticky-top">
      <div class="container">
        <a class="navbar-brand fw-bold d-flex align-items-center gap-2" href="{% url 'shop2:product-list' %}">
          <i class="bi bi-eyeglasses"></i> LensHive
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div id="nav" class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto">
            <li class="nav-item"><a class="nav-link" href="{% url 'shop2:product-list' %}">All Products</a></li>
            <li class="nav-item"><a class="nav-link" href="{% url 'shop2:product-add' %}">Add Product</a></li>
          </ul>

          <form class="d-flex" role="search" action="{% url 'shop2:product-list' %}">
            <input class="form-control me-2" type="search" name="q" value="{{ current_q|default:'' }}" placeholder="Search…">
            {% if current_sort %}<input type="hidden" name="sort" value="{{ current_sort }}">{% endif %}
            <button class="btn btn-outline-primary" type="submit"><i class="bi bi-search"></i></button>
          </form>

          <div class="vr mx-3 d-none d-md-block"></div>

          <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" id="themeSwitch">
            <label class="form-check-label" for="themeSwitch"><i class="bi bi-moon-stars"></i></label>
          </div>
        </div>
      </div>
    </nav>

    {% block hero %}{% endblock %}

    <main class="container py-4">
      {% block content %}{% endblock %}
    </main>

    <footer class="border-top py-4 mt-5">
      <div class="container d-flex justify-content-between align-items-center small">
        <span class="text-muted">© {{ now|date:"Y" }} LensHive</span>
        <a class="text-decoration-none" href="{% url 'shop2:product-add' %}">
          <i class="bi bi-plus-circle"></i> Add Product
        </a>
      </div>
    </footer>

    <script>
      // Persist dark/light preference
      (function () {
        const key = "lh-theme";
        const html = document.documentElement;
        const saved = localStorage.getItem(key);
        if (saved) html.setAttribute("data-bs-theme", saved);
        const switcher = document.getElementById("themeSwitch");
        if (switcher) {
          switcher.checked = (html.getAttribute("data-bs-theme") === "dark");
          switcher.addEventListener("change", () => {
            const next = switcher.checked ? "dark" : "light";
            html.setAttribute("data-bs-theme", next);
            localStorage.setItem(key, next);
          });
        }
      })();
    </script>
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
      crossorigin="anonymous"
    ></script>
  </body>
</html>
"""

product_list_html = """{% extends 'base.html' %}

{% block hero %}
<section class="hero-gradient border-bottom">
  <div class="container py-5">
    <div class="row align-items-center g-4">
      <div class="col-md-7">
        <h1 class="display-6 fw-bold mb-2">Find your next frame</h1>
        <p class="lead mb-0 text-opacity-75">Search, sort, and filter modern eyewear — fast.</p>
      </div>
      <div class="col-md-5 d-flex justify-content-md-end gap-2">
        <a class="btn btn-primary btn-lg" href="{% url 'shop2:product-add' %}">
          <i class="bi bi-plus-circle"></i> Add Product
        </a>
        <button class="btn btn-outline-light btn-lg" data-bs-toggle="offcanvas" data-bs-target="#filters">
          <i class="bi bi-sliders"></i> Filters
        </button>
      </div>
    </div>
  </div>
</section>
{% endblock %}

{% block content %}

<div class="d-flex flex-wrap gap-2 align-items-center justify-content-between mb-3">
  <div class="text-muted small">{{ page_obj.paginator.count }} items</div>
  <form class="d-flex gap-2 align-items-center" method="get">
    <input type="hidden" name="q" value="{{ current_q|default:'' }}">
    <select class="form-select" name="sort">
      <option value="" {% if not current_sort %}selected{% endif %}>Sort: Newest</option>
      <option value="-created_at" {% if current_sort == '-created_at' %}selected{% endif %}>Newest</option>
      <option value="created_at" {% if current_sort == 'created_at' %}selected{% endif %}>Oldest</option>
      <option value="price" {% if current_sort == 'price' %}selected{% endif %}>Price: Low → High</option>
      <option value="-price" {% if current_sort == '-price' %}selected{% endif %}>Price: High → Low</option>
      <option value="name" {% if current_sort == 'name' %}selected{% endif %}>Name A–Z</option>
      <option value="-name" {% if current_sort == '-name' %}selected{% endif %}>Name Z–A</option>
    </select>
    <select class="form-select" name="per_page">
      {% for n in '12,24,36,48'.split(',') %}
        <option value="{{ n }}" {% if per_page|stringformat:'s' == n %}selected{% endif %}>{{ n }}/page</option>
      {% endfor %}
    </select>
    <button class="btn btn-outline-primary" type="submit">Apply</button>
  </form>
</div>

<!-- Offcanvas Filters -->
<div class="offcanvas offcanvas-end" tabindex="-1" id="filters">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title"><i class="bi bi-sliders"></i> Filters</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <form method="get" class="vstack gap-3">
      <input type="hidden" name="q" value="{{ current_q|default:'' }}">
      <input type="hidden" name="sort" value="{{ current_sort|default:'' }}">
      <input type="hidden" name="per_page" value="{{ per_page|default:12 }}">

      <div>
        <label class="form-label">Style</label>
        <div class="d-flex flex-wrap gap-2">
          {% for s in styles %}
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="style" id="style-{{ forloop.counter }}" value="{{ s }}"
                     {% if s in sel_styles %}checked{% endif %}>
              <label class="form-check-label" for="style-{{ forloop.counter }}">{{ s|default:"(unspecified)" }}</label>
            </div>
          {% empty %}
            <div class="text-muted small">No style values yet.</div>
          {% endfor %}
        </div>
      </div>

      <div>
        <label class="form-label">Material</label>
        <div class="d-flex flex-wrap gap-2">
          {% for m in materials %}
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="material" id="mat-{{ forloop.counter }}" value="{{ m }}"
                     {% if m in sel_materials %}checked{% endif %}>
              <label class="form-check-label" for="mat-{{ forloop.counter }}">{{ m|default:"(unspecified)" }}</label>
            </div>
          {% empty %}
            <div class="text-muted small">No material values yet.</div>
          {% endfor %}
        </div>
      </div>

      <div>
        <label class="form-label">Price range</label>
        <div class="input-group">
          <span class="input-group-text">₹</span>
          <input class="form-control" type="number" min="0" step="1" placeholder="Min" name="min_price" value="{{ min_price|default:'' }}">
          <span class="input-group-text">to</span>
          <input class="form-control" type="number" min="0" step="1" placeholder="Max" name="max_price" value="{{ max_price|default:'' }}">
        </div>
      </div>

      <div class="d-grid">
        <button class="btn btn-primary" type="submit"><i class="bi bi-filter"></i> Apply filters</button>
      </div>
    </form>
  </div>
</div>

{% if products %}
  <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-xl-4 g-4">
    {% for product in products %}
      <div class="col">
        <div class="card h-100 lh-card">
          <div class="ratio ratio-4x3 overflow-hidden">
            <img class="w-100 h-100 object-fit-cover"
                 src="{{ product.image_url|default:'https://via.placeholder.com/800x600?text=LensHive' }}"
                 alt="{{ product.name }}"
                 onerror="this.src='https://via.placeholder.com/800x600?text=LensHive'">
          </div>
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between align-items-start mb-1">
              <h5 class="card-title mb-0 lh-1 text-truncate">{{ product.name }}</h5>
              <span class="badge text-bg-light border fw-semibold">₹{{ product.price }}</span>
            </div>
            <div class="small text-muted mb-2">
              {% if product.stock_quantity > 0 %}
                <span class="badge text-bg-success-subtle border">In stock: {{ product.stock_quantity }}</span>
              {% else %}
                <span class="badge text-bg-danger-subtle border">Out of stock</span>
              {% endif %}
            </div>
            <p class="card-text lh-1 text-muted line-clamp-2">{{ product.description|default:"" }}</p>
            <div class="mt-auto d-flex gap-2">
              <a class="btn btn-sm btn-primary flex-fill" href="{% url 'shop2:product-detail' product.pk %}">
                <i class="bi bi-eye"></i> View
              </a>
              <button class="btn btn-sm btn-outline-secondary flex-fill" type="button" onclick="lhToast('Added to cart (demo)')">
                <i class="bi bi-bag-plus"></i> Add
              </button>
            </div>
          </div>
        </div>
      </div>
    {% endfor %}
  </div>

  {% if is_paginated %}
    <nav class="mt-4" aria-label="Product pagination">
      <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?{{ qs }}&page={{ page_obj.previous_page_number }}">Previous</a>
          </li>
        {% else %}
          <li class="page-item disabled"><span class="page-link">Previous</span></li>
        {% endif %}

        {% for num in paginator.page_range %}
          {% if num == page_obj.number %}
            <li class="page-item active"><span class="page-link">{{ num }}</span></li>
          {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
            <li class="page-item"><a class="page-link" href="?{{ qs }}&page={{ num }}">{{ num }}</a></li>
          {% endif %}
        {% endfor %}

        {% if page_obj.has_next %}
          <li class="page-item">
            <a class="page-link" href="?{{ qs }}&page={{ page_obj.next_page_number }}">Next</a>
          </li>
        {% else %}
          <li class="page-item disabled"><span class="page-link">Next</span></li>
        {% endif %}
      </ul>
    </nav>
  {% endif %}
{% else %}
  <div class="text-center py-5">
    <h2 class="h4">No products found</h2>
    <p class="text-muted">Try a different search or add a product.</p>
    <a class="btn btn-primary" href="{% url 'shop2:product-add' %}"><i class="bi bi-plus-circle"></i> Add Product</a>
  </div>
{% endif %}

<!-- Toast (demo) -->
<div class="toast-container position-fixed bottom-0 end-0 p-3">
  <div id="lhToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header">
      <i class="bi bi-check-circle-fill me-2 text-success"></i>
      <strong class="me-auto">LensHive</strong>
      <small>now</small>
      <button type="button" class="btn-close ms-2 mb-1" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">Done.</div>
  </div>
</div>
<script>
  function lhToast(msg) {
    const t = document.getElementById('lhToast');
    t.querySelector('.toast-body').textContent = msg || 'Done.';
    bootstrap.Toast.getOrCreateInstance(t).show();
  }
</script>

{% endblock %}
"""

product_detail_html = """{% extends 'base.html' %}
{% block content %}
<nav aria-label="breadcrumb" class="mb-3">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="{% url 'shop2:product-list' %}">Products</a></li>
    <li class="breadcrumb-item active" aria-current="page">{{ product.name }}</li>
  </ol>
</nav>

<div class="row g-4 align-items-start">
  <div class="col-lg-6">
    <div class="ratio ratio-4x3 rounded border overflow-hidden">
      <img class="w-100 h-100 object-fit-cover"
           src="{{ product.image_url|default:'https://via.placeholder.com/900x600?text=LensHive' }}"
           alt="{{ product.name }}"
           onerror="this.src='https://via.placeholder.com/900x600?text=LensHive'">
    </div>
  </div>
  <div class="col-lg-6">
    <h1 class="h3">{{ product.name }}</h1>
    <div class="fs-3 fw-semibold mb-3">₹{{ product.price }}</div>

    <div class="small text-muted mb-2">
      {% if product.stock_quantity > 0 %}
        <span class="badge text-bg-success-subtle border">In stock: {{ product.stock_quantity }}</span>
      {% else %}
        <span class="badge text-bg-danger-subtle border">Out of stock</span>
      {% endif %}
    </div>

    <dl class="row small">
      {% if product.style %}<dt class="col-sm-3">Style</dt><dd class="col-sm-9">{{ product.style }}</dd>{% endif %}
      {% if product.material %}<dt class="col-sm-3">Material</dt><dd class="col-sm-9">{{ product.material }}</dd>{% endif %}
    </dl>

    <p class="mt-3">{{ product.description }}</p>

    <div class="d-flex gap-2 mt-4">
      <button class="btn btn-primary" type="button" onclick="lhToast('Added to cart (demo)')">
        <i class="bi bi-bag-plus"></i> Add to Cart
      </button>
      <a class="btn btn-outline-secondary" href="{% url 'shop2:product-list' %}">Back to list</a>
    </div>
  </div>
</div>
{% endblock %}
"""

product_form_html = """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-lg-8 col-xl-6">
    <div class="card shadow-sm">
      <div class="card-body">
        <h1 class="h4 mb-3"><i class="bi bi-plus-circle"></i> Add a New Product</h1>
        <form method="post" novalidate>
          {% csrf_token %}
          {{ form.as_p }}
          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary">Save</button>
            <a href="{% url 'shop2:product-list' %}" class="btn btn-outline-secondary">Cancel</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}
"""

app_css = """/* LensHive mini theme */
.hero-gradient {
  background: radial-gradient(1200px 600px at 10% -10%, rgba(13,110,253,.25), transparent),
              radial-gradient(1000px 500px at 110% -20%, rgba(255,193,7,.25), transparent);
}
.lh-card { transition: transform .15s ease, box-shadow .15s ease; }
.lh-card:hover { transform: translateY(-2px); box-shadow: 0 .5rem 1.25rem rgba(0,0,0,.08) !important; }
.line-clamp-2 {
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.object-fit-cover { object-fit: cover; }
"""

views_py = """from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from .forms import ProductForm
from .models import Products

class ProductCreateView(CreateView):
    model = Products
    form_class = ProductForm
    template_name = 'shop2/product_form.html'
    success_url = reverse_lazy('shop2:product-list')

class ProductListView(ListView):
    model = Products
    template_name = 'shop2/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_paginate_by(self, queryset):
        try:
            per = int(self.request.GET.get('per_page') or self.paginate_by)
            return min(max(per, 12), 48)
        except (TypeError, ValueError):
            return self.paginate_by

    def get_queryset(self):
        qs = Products.objects.all()

        # search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        # filters (multiple values supported)
        styles = self.request.GET.getlist('style') or []
        if styles:
            qs = qs.filter(style__in=styles)

        materials = self.request.GET.getlist('material') or []
        if materials:
            qs = qs.filter(material__in=materials)

        # price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            try:
                qs = qs.filter(price__gte=min_price)
            except Exception:
                pass
        if max_price:
            try:
                qs = qs.filter(price__lte=max_price)
            except Exception:
                pass

        # sort
        sort = self.request.GET.get('sort') or ''
        allowed = {'price', '-price', 'name', '-name', 'created_at', '-created_at', 'product_id', '-product_id'}
        if sort in allowed:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by('-product_id')

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        req = self.request

        # distinct lists for filters
        ctx['styles'] = (Products.objects.exclude(style__isnull=True)
                         .exclude(style__exact='')
                         .values_list('style', flat=True).distinct().order_by('style'))
        ctx['materials'] = (Products.objects.exclude(material__isnull=True)
                            .exclude(material__exact='')
                            .values_list('material', flat=True).distinct().order_by('material'))

        # current selections
        ctx['current_q'] = req.GET.get('q', '')
        ctx['current_sort'] = req.GET.get('sort', '')
        ctx['per_page'] = req.GET.get('per_page', self.paginate_by)
        ctx['sel_styles'] = req.GET.getlist('style')
        ctx['sel_materials'] = req.GET.getlist('material')
        ctx['min_price'] = req.GET.get('min_price', '')
        ctx['max_price'] = req.GET.get('max_price', '')

        # querystring without page for pagination links
        qs_params = req.GET.copy()
        qs_params.pop('page', None)
        ctx['qs'] = qs_params.urlencode()
        return ctx

class ProductDetailView(DetailView):
    model = Products
    template_name = 'shop2/product_detail.html'
    context_object_name = 'product'
"""

write("templates/base.html", base_html)
write("templates/shop2/product_list.html", product_list_html)
write("templates/shop2/product_detail.html", product_detail_html)
write("templates/shop2/product_form.html", product_form_html)
write("shop2/static/shop2/app.css", app_css)
write("shop2/views.py", views_py)

# Try to commit (optional)
try:
    files = [
        "templates/base.html",
        "templates/shop2/product_list.html",
        "templates/shop2/product_detail.html",
        "templates/shop2/product_form.html",
        "shop2/static/shop2/app.css",
        "shop2/views.py",
    ]
    subprocess.run(["git", "add"] + files, check=True)
    subprocess.run(["git", "commit", "-m", "Polish UI: hero, icons, filters, hover effects, better pagination"], check=True)
    print("\nCommitted changes.")
except Exception as e:
    print("\nSkipped git commit (you can commit manually).", e)

print("\n✅ Done. Now run:  python manage.py runserver")
