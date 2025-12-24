from django.shortcuts import render

# Create your views here.

def gradient_view(request):

    num_shades = 50
    
    colors = {
        'Black': generate_gradient(0, 0, 0, num_shades),
        'Red': generate_gradient(255, 0, 123, num_shades),
        'Blue': generate_gradient(0, 123, 255, num_shades),
        'Green': generate_gradient(0, 255, 123, num_shades),
    }
    
    rows = []
    for i in range(num_shades):
        row = [
            colors['Black'][i],
            colors['Red'][i],
            colors['Blue'][i],
            colors['Green'][i],
        ]
        rows.append(row)
    
    context = {
        'headers': ['Black', 'Red', 'Blue', 'Green'],
        'rows': rows,
    }
    
    return render(request, 'gradient.html', context)


def generate_gradient(r, g, b, num_shades):
    shades = []
    for i in range(num_shades):
        intensity = i / (num_shades + 1)
        
        shade_r = int(r * intensity)
        shade_g = int(g * intensity)
        shade_b = int(b * intensity)
        
        # Formater en RGB CSS
        shades.append(f'rgb({shade_r}, {shade_g}, {shade_b})')
    
    return shades
