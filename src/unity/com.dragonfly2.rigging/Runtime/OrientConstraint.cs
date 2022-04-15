using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OrientConstraint : MonoBehaviour
{
    [Range(0f, 1f)] public float weight = 1.0f;
    public Transform target;
    public bool maintainOffset;
    private Quaternion restRotation;
    private Quaternion targetRotation;
    void Start()
    {
        restRotation = transform.rotation;
    }

    void LateUpdate()
    {
        if (weight <= 0f)
        {
            return;
        }

        targetRotation = target.rotation;
        
        if (maintainOffset)
        {
            targetRotation = target.rotation * restRotation;
        }

        transform.rotation = Quaternion.Slerp(restRotation, targetRotation, weight);
    }
}
