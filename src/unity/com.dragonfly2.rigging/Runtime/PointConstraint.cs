using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Dragonfly
{
    public class PointConstraint : MonoBehaviour
    {
        [Range(0f, 1f)] public float weight = 1f;
        public Transform target;
        public bool maintainOffset;
        
        private Vector3 restPosition;
        private Vector3 targetPosition;

        void Start()
        {
            restPosition = transform.localPosition;
        }

        void LateUpdate()
        {
            if (weight <= 0f)
            {
                return;
            }

            targetPosition = target.position * weight;
            
            if (maintainOffset)
            {
                if (transform.parent)
                {
                    targetPosition += transform.parent.InverseTransformPoint(restPosition);
                }
                else
                {
                    targetPosition += restPosition;
                }
            }

            transform.position = targetPosition;
        }
    }
}


