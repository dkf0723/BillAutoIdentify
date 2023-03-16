package com.example.demo.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "發票圖檔" )
public class BillPicture {
    @Id
    @Column(name = "發票號碼",length = 18,nullable = false)
    private String billNumber;

    @Column(name = "圖檔")
    private String picture;
}
