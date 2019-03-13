import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib import patches, lines

def draw_circle(ax, radius, origin):
    x,y = origin
    circle = plt.Circle((x, y), radius, color='gray', fill=False, linestyle='dashed')
    return ax.add_artist(circle)

def draw_angle(ax, angle_rad, radius, origin, show_label=False, show_head=False, linestyle='solid'):
    x,y = origin
    head_length = 0.025 if show_head else 0
    dx = (radius - head_length) * math.cos(angle_rad)
    dy = (radius - head_length) * math.sin(angle_rad)
    if show_label:
        label = f"$ R = {radius:.3f}m $"
        label_x = x + radius/1.5 * math.cos(angle_rad)
        label_y = y + radius/1.5 * math.sin(angle_rad)
        ax_label = ax.annotate(label, xy=(label_x,label_y), xytext=(label_x + 0.025, label_y + 0.025), size=10)
        
    return ax.arrow(x, y, dx, dy, head_width=head_length, head_length=head_length, fc='k', ec='k', linestyle=linestyle)
    
def draw_displacement(ax, angle_rad, radius, origin, theta1=0, show_label=False, show_head=False, show_arc=True, linestyle="solid"):
    x,y = origin
    inner_radius = radius
    
    angle = np.rad2deg(angle_rad)
    elements = []
    
    if show_arc:
        arc = Arc((x, y), inner_radius * 2, inner_radius * 2, theta1=theta1, theta2=min(360, np.rad2deg(angle_rad)), linestyle=linestyle)
        elements.append(ax.add_patch(arc))
    
    if show_label:
        label = f"$ \Delta\\theta = \\theta_f - \\theta_i = {angle_rad:.3f} ({angle:.0f}°)$"
        label_x = x + inner_radius * math.cos(angle_rad)
        label_y = y + inner_radius * math.sin(angle_rad)
        elements.append(ax.annotate(label, xy=(label_x,label_y), xytext=(label_x + 0.025, label_y + 0.025), size=10))
    
    if show_head:
        head_length = 0.015
        head_dx = head_length * math.cos(angle_rad + math.pi / 2)
        head_dy = head_length * math.sin(angle_rad + math.pi / 2)
        head_x = x + inner_radius * math.cos(angle_rad) - head_dx
        head_y = y + inner_radius * math.sin(angle_rad) - head_dy
        elements.append(ax.arrow(head_x, head_y, head_dx * 1e-10, head_dy * 1e-10,
                            head_width=head_length, head_length=head_length))
    
    return elements
    
def show_displacement(figure, ax, displacement, pos=(0.5, 0.5), radius=0.3):    
    x, y = pos
    circle = draw_circle(ax, radius, (x,y))
    
    angle_rad, angle_deg = displacement, np.rad2deg(displacement)
    angle0_line = draw_angle(ax, 0, radius, (x,y), linestyle='dashed')
    angle_line = draw_angle(ax, angle_rad, radius, (x,y), show_label=True)
    displacement_elements = draw_displacement(ax, angle_rad, radius / 4, (x,y), show_label=True, show_head=True)
    
    return (circle, angle0_line, angle_line, *displacement_elements)

def draw_particle(ax, position, radius=0.025, color='b'):
    x,y = position
    particle = patches.Circle((x,y), radius, color=color)
    return ax.add_patch(particle)

def draw_labeled_arrow(ax, origin, vector, label_format="", color="black"):
    x,y = origin
    dx,dy = vector
    elements = []
    elements.append(ax.arrow(x, y, dx, dy, head_width=0.015, head_length=0.015, color=color))
    elements.append(ax.annotate(label_format, xy=(x + dx * 0.5, y + dy * 0.5 - 0.025)))
    return elements

def draw_rect(ax, position, width=0.6, height=0.036, angle=0, show_length=True, arrow_length=None):
    if not arrow_length:
        arrow_length = width

    x,y = position
    rect = patches.Rectangle((x, y), width, height, linewidth=1,
                             edgecolor='black', facecolor='none', angle=angle)

    if show_length:
        arrow_dx = np.sin(np.deg2rad(angle + 90)) * (arrow_length - 0.015)
        arrow_dy = -np.cos(np.deg2rad(angle + 90)) * (arrow_length - 0.015)
        draw_labeled_arrow(ax, (x, y), (arrow_dx, arrow_dy), label_format=f"{arrow_length:.3f}m")

    return ax.add_patch(rect)