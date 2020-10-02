# frappe-inventory

This project is done using Flask, Flask-sqlalchemy, SQLite

                <th>warehouse</th>
                <th>product_name</th>
                <th>production_quantity</th>
                <td>{{ i.User1.warehouse }}</td>
                <td>{{ i.User1.product_name }}</td>
                <td>{{ i.User1.quantity }}</td>
                    <thead>
        <th>warehouse</th>
        <th>product_name</th>
        <th>production_quantity</th>
    </thead>
    <tbody>
        {% for i in user_info %}
        <tr>
            <td>{{ i.warehouse }}</td>
            <td>{{ i.product_name }}</td>
            <td>{{ i.quantity }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>