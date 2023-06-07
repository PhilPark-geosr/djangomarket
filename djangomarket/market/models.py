from django.db import models

# Create your models here.
"""
public class Member {
 @Id @GeneratedValue
 @Column(name = "member_id")
 private Long id;
 private String name;
 @Embedded
 private Address address;
 @OneToMany(mappedBy = "member")
 private List<Order> orders = new ArrayList<>();
}
"""
# class Member(models.Model):
#     name = models.CharField()
#     address = models.TextField()
#     orders = models.()