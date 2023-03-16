package com.example.demo.model.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public class BillDetailId implements Serializable {

    @Id
    @Column(name = "發票號碼",length = 18,nullable= false)
    private String number;

    @Id
    @Column(name = "項次",nullable = false)
    private Integer column;

}
